
import os
import shutil
import platform
import argparse
from pathlib import Path

from pathlib import Path

def enforce_pdf_path(file_name: str) -> str:
    path = str(Path(path).as_posix())
    path = Path(file_name)
    return str(path.with_suffix('.pdf'))





def enforce_dir_path(dir_path: str) -> str:
    path = str(Path(path).as_posix())
    path = Path(dir_path)
    return str(path.as_posix().rstrip('/')) + '/'



def is_dir_valid(path: str) -> str:
    path = str(Path(path).as_posix())
    if(not os.path.isdir(path)):
        if(not path == ""):
            raise argparse.ArgumentTypeError(f"`{path}` is not a valid directory or does not exist in given context")
    return path

def is_valid_file(path: str) -> str:
    path = str(Path(path).as_posix())
    if(not os.path.isfile(path)):
        if(not path == ""):
            raise argparse.ArgumentTypeError(f"`{path}` is not a valid file to in the given context.")
    return path

def get_soffice_path() -> str | None:
    """
    Try to find the 'soffice' executable on the current system.
    Returns full path or None if not found.
    """
    # Try using the PATH first
    soffice = shutil.which("soffice")
    if soffice:
        return soffice

    # Try platform-specific defaults
    system = platform.system()
    if system == "Windows":
        # Adjust if LibreOffice is installed elsewhere
        possible_paths = [
            Path("C:/Program Files/LibreOffice/program/soffice.exe"),
            Path("C:/Program Files (x86)/LibreOffice/program/soffice.exe")
        ]
    elif system == "Darwin":  # macOS
        possible_paths = [
            Path("/Applications/LibreOffice.app/Contents/MacOS/soffice")
        ]
    elif system == "Linux":
        possible_paths = [Path("/usr/bin/soffice")]
    else:
        return None

    for path in possible_paths:
        if path.exists():
            return str(path)

    return None