import subprocess

from tools.util import sisyphus_register, sisyphus_tool


class ShellTool:
    def __init__(self):
        sisyphus_register(self)

    @sisyphus_tool
    def execute_command(self, command: str):
        """Execute a shell command"""
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        return process.stdout.read(-1)
