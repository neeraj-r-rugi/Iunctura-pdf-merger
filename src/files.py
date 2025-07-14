from pathlib import Path

def get_pdf_files(path: str, extra_files: list, walk:str, sort:str, exclude_path:list) ->tuple:
    if(walk):
        pdf_files = [str(f) for f in Path(path).rglob('*.pdf') if f.is_file()]
    else:
        pdf_files = [str(f) for f in Path(path).glob('*.pdf') if f.is_file()]
    
    if(sort == "asec"):
        pdf_files = sorted(pdf_files)
    else:
        pdf_files = sorted(pdf_files, reverse=True)
    
    if(extra_files):
        pdf_files += extra_files
        
    for item in exclude_path:
        if item in pdf_files:
            pdf_files.remove(item)
    
    return tuple(pdf_files)

def get_all_files(path: str, extra_files: list, walk:str, sort:str, exclude_path:list):
    if(walk):
        all_files = [str(f) for f in Path(path).rglob('*') if f.is_file()]
    else:
        all_files = [str(f) for f in Path(path).glob('*') if f.is_file()]
    
    if(sort == "asec"):
        all_files = sorted(all_files)
    else:
        all_files = sorted(all_files, reverse=True)
    
    if(extra_files):
        all_files += all_files
        
    for item in exclude_path:
        if item in all_files:
            all_files.remove(item)
    return tuple(all_files)

    