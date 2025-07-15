from pathlib import Path

def get_pdf_files(path: str, extra_files: list, walk:str, sort:str, exclude_path:list, priority:str) ->tuple:
    pdf_files = []
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
        
    for item in exclude_path:
        if item in pdf_files:
            pdf_files.remove(item)
    
    return (pdf_files)

def get_all_files(path: str, extra_files: list, walk:str, sort:str, exclude_path:list, priority: str):
    all_files = []
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
        
    for item in exclude_path:
        if item in all_files:
            all_files.remove(item)
            
    return (all_files)


def merge_filtered_path(all_files: list, filtered_paths: list) -> list:
    path_map = {
        Path(p).with_suffix(".pdf").name.lower(): p
        for p in filtered_paths
    }

    result = []
    for file in all_files:
        file_name_pdf = Path(file).with_suffix(".pdf").name.lower()
        replacement = path_map.get(file_name_pdf, file)
        result.append(replacement)

    return result
        
    

    