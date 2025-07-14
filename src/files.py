from pathlib import Path

def get_pdf_files(path: str, extra_files: list, walk:str, sort:str) ->tuple:
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
    return tuple(pdf_files)

def get_all_files(path: str, extra_files: list, walk:str, sort:str):
    if(walk):
        pdf_files = [str(f) for f in Path(path).rglob('*') if f.is_file()]
    else:
        pdf_files = [str(f) for f in Path(path).glob('*') if f.is_file()]
    
    if(sort == "asec"):
        pdf_files = sorted(pdf_files)
    else:
        pdf_files = sorted(pdf_files, reverse=True)
    
    if(extra_files):
        pdf_files += extra_files
    return tuple(pdf_files)
    