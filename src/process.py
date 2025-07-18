
import os
import shutil
import platform
import argparse
from pathlib import Path

from pathlib import Path

def enforce_pdf_path(file_name: str) -> str:
    
    file_name = Path(file_name).with_suffix('.pdf').as_posix()
    return file_name





def enforce_dir_path(dir_path: str) -> str:
    
    path = Path(dir_path)
    path = str(path.as_posix().rstrip('/')) + '/'
    return path



def is_dir_valid(path: str) -> str:
    
    if(path and (not os.path.isdir(path))):
        raise argparse.ArgumentTypeError(f"`{path}` is not a valid directory or does not exist in given context")

    if(path):
        path = Path(path).as_posix().rstrip('/') + '/'
        return path
    else:
        return path

def is_valid_file(path: str) -> str:
    if(path and (not os.path.isfile(path))):
        raise argparse.ArgumentTypeError(f"`{path}` is not a valid file or does not exist in given context")
        
    if(path):
        path = Path(path).as_posix()
        return path
    else:
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