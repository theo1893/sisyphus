import threading

from fastapi import FastAPI
from loguru import logger

from tools.browser.browser_api import BrowserAutomation
from tools.browser.browser_tool import BrowserTool

# Global variable to store the subprocess
_uvicorn_process = None
_server_thread = None


def initialize():
    _ = BrowserTool()

    # Create singleton instance
    automation_service = BrowserAutomation()

    # Create API app
    api_app = FastAPI()

    @api_app.get("/api")
    async def health_check():
        return {"status": "ok", "message": "API server is running"}

    api_app.include_router(automation_service.router, prefix="/api")

    def start_uvicorn_thread():
        """Start uvicorn server in a separate thread (alternative approach)."""
        global _server_thread

        if _server_thread is not None and _server_thread.is_alive():
            logger.info("Uvicorn server thread already running")
            return

        def run_server():
            try:
                import uvicorn

                logger.info("Starting uvicorn server in thread...")
                uvicorn.run(api_app, host="0.0.0.0", port=8000, log_level="info")
            except Exception as e:
                logger.error(f"Error in uvicorn server thread: {e}")

        _server_thread = threading.Thread(target=run_server, daemon=True)
        _server_thread.start()
        logger.info("Uvicorn server thread started")

    start_uvicorn_thread()
