# Iunctura PDF Merger: A powerful command-line tool for merging and converting PDF files with flexible file handling and organization options. Tired of manually combining lecture slides or documents? Iunctura simplifies the process by offering seamless PDF merging, file conversion, and recursive directory processing. 
# Copyright (C) 2024 NEERAJ R RUGI

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from pathlib import Path

def get_pdf_files(path: str, extra_files: list, walk:str, sort:str, exclude_path:list, priority:str) ->tuple:
    try:
        pdf_files = []
        if(path and any(dir.strip() for dir in path)):
            if(not isinstance(path, list)):
                path = [path]
            for dir in path: 
                if(walk):
                    pdf_files += [str(f) for f in Path(dir).rglob('*.pdf') if f.is_file()]
                else:
                    pdf_files += [str(f) for f in Path(dir).glob('*.pdf') if f.is_file()]
            
            if(sort == "asec"):
                pdf_files = sorted(pdf_files, key=lambda f: Path(f).name.lower())
            elif(sort == "desc"):
                pdf_files = sorted(pdf_files, key=lambda f: Path(f).name.lower(),reverse=True)
            else:
                pass
    
        
    
        if(extra_files):
            if(priority == "dir"):
                pdf_files += extra_files
            else:
                pdf_files = extra_files + pdf_files
            
        exclude_names = set(Path(p).name.lower() for p in exclude_path)
        pdf_files = [f for f in pdf_files if Path(f).name.lower() not in exclude_names]
    except  Exception as e:
        print(f"Failed to fetch PDF Files: {e}")
    
    return (pdf_files)
    

def get_all_files(path: list, extra_files: list, walk:str, sort:str, exclude_path:list, priority: str):
    try:
        all_files = []
        if(path and any(dir.strip() for dir in path)):
            if(not isinstance(path, list)):
                path = [path]
            for dir in path:
                if(walk):
                    all_files += [str(f) for f in Path(dir).rglob('*') if f.is_file()]
                else:
                    all_files += [str(f) for f in Path(dir).glob('*') if f.is_file()]
            
            if(sort == "asec"):
                all_files = sorted(all_files, key=lambda f: Path(f).name.lower())
            elif(sort == "desc"):
                all_files = sorted(all_files, key=lambda f: Path(f).name.lower(), reverse=True)
            else:
                pass
        
        if(extra_files):
            if(priority == "dir"):
                all_files += extra_files
            else:
                all_files = extra_files + all_files
            
        exclude_names = set(Path(p).name.lower() for p in exclude_path)
        all_files = [f for f in all_files if Path(f).name.lower() not in exclude_names]
    except Exception as e:
        print(f"Failed to Fetch all files: {e}")
            
    return (all_files)


def merge_filtered_path(all_files: list, filtered_paths: list) -> list:
    try:

        path_map = {
            Path(p).stem.lower(): p
            for p in filtered_paths
            if Path(p).suffix.lower() == ".pdf"
        }

        result = []
        for file in all_files:
            path = Path(file)
            if path.suffix.lower() != ".pdf":
                # This was a converted file, try to replace it
                replacement = path_map.get(path.stem.lower(), file)
                result.append(replacement)
            else:
                # Already a .pdf — keep as is
                result.append(file)

        return result
    except Exception as e:
        print(f"Failed to merge and filter files: {e}")
        return all_files
        
    

    