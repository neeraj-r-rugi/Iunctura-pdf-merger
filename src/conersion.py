import pypdf as pdf
import os
from . import process
from pathlib import Path
import subprocess
import sys

ALLOWED_FORMATS = [
    # Text Documents
    ".doc", ".docx", ".odt", ".rtf", ".txt", ".fodt", ".html", ".htm",
    
    # Spreadsheets
    ".xls", ".xlsx", ".ods", ".csv", ".fods",
    
    # Presentations
    ".ppt", ".pptx", ".odp", ".fodp",
    
    # Drawings
    ".odg", ".fodg", ".svg", ".emf", ".wmf",
    
    # Other Office Formats
    ".xml", ".xhtml", ".epub",
]

def save_as_pdf(files: list, output_name:str):
    if(files):
        merger = pdf.PdfWriter()
        for file in files:
            merger.append(str(file))
            
        merger.write(output_name)
    
    
def convert_to_pdf(paths: list, output_dir: str)-> tuple:
    soffice = process.get_soffice_path()
    if not soffice:
        print("Fatal Error: LibreOffice 'soffice' not found on your system.\nVerify if it exists on your PATH.")
        sys.exit()

    filtered_paths = []
    for item in paths:
        file = Path(item)
        if file.suffix.lower() in ALLOWED_FORMATS:
            filtered_paths.append(file)
        else:
           pass
    if not filtered_paths:
        print("Given Context Consists of all PDF files or some non compliant files with PDF files. Hence No Conversion is done\n\n")
        temp_dir = Path(output_dir)
        temp_dir.mkdir(exist_ok=True, parents= True)
        return ""
    
    temp_dir = Path(output_dir)
    temp_dir.mkdir(exist_ok=True, parents= True)
    print(f"Output for Conversion of files to PDF from LibreOffice:\n{"#"*50}")
    for input_path in filtered_paths:
        try:
            subprocess.run([
                soffice, "--headless", "--convert-to", "pdf",
                str(input_path), "--outdir", str(temp_dir)
            ], check=True)
            print(f"-------> [Converted] {input_path} to PDF\n{"*"*75}")
        except subprocess.CalledProcessError as e:
            print(f"Error converting `{input_path}`: {e}")
            
    temp = []
    
    for item in filtered_paths:
        item = item.with_suffix(".pdf")
        item = f"{output_dir}"+str(Path(item).name)
        temp.append(item)
        
    filtered_paths = temp
    print(f"{"#"*50}")
    return filtered_paths
    

    