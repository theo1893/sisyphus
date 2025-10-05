import os
import uuid
from pathlib import Path
from typing import Optional

from tools.util import sisyphus_tool, sisyphus_register


class LocalFS:
    cwd: str
    session: str

    def __init__(self, cwd: str = os.path.join(os.getcwd(), "workspace"), session: str = str(uuid.uuid4())):
        self.cwd = cwd
        self.session = session
        self.session_dir = Path(self.cwd) / self.session
        self.session_dir.mkdir(parents=True, exist_ok=True)

        sisyphus_register(self)

    def _resolve_path(self, file_name: str) -> Path:
        return self.session_dir / Path(file_name)

    @sisyphus_tool
    def create_file(self, file_name: str, content: str) -> bool:
        """Create file with content"""
        try:
            file_path = self._resolve_path(file_name)
            file_path.parent.mkdir(parents=True, exist_ok=True)

            if file_path.exists():
                raise FileExistsError(f"File already exists: {file_path}")

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            return True

        except Exception as e:
            print(f"Error creating file {file_name}: {str(e)}")
            return False

    @sisyphus_tool
    def modify_file(self, file_name: str, old_content: str, new_content: str) -> bool:
        """Modify old file content with new content"""
        try:
            file_path = self._resolve_path(file_name)

            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")

            with open(file_path, 'r', encoding='utf-8') as f:
                current_content = f.read()

            if old_content in current_content:
                modified_content = current_content.replace(old_content, new_content)

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(modified_content)

                return True
            else:
                print(f"Old content not found in file {file_name}")
                return False

        except Exception as e:
            print(f"Error modifying file {file_name}: {str(e)}")
            return False

    @sisyphus_tool
    def read_file(self, file_name: str) -> Optional[str]:
        """Read file content"""
        try:
            file_path = self._resolve_path(file_name)

            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")

            if not file_path.is_file():
                raise IsADirectoryError(f"Path is not a file: {file_path}")

            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()

        except Exception as e:
            print(f"Error reading file {file_name}: {str(e)}")
            return None

    @sisyphus_tool
    def write_file(self, file_name: str, content: str) -> bool:
        """Append content to file"""
        try:
            file_path = self._resolve_path(file_name)
            file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(content)

            return True

        except Exception as e:
            print(f"Error writing file {file_name}: {str(e)}")
            return False
