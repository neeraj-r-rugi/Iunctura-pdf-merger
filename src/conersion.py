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

def save_pdf(paths: list, output_name:str):
    merger = pdf.PdfWriter()
    for file in paths:
        merger.append(str(file))
    
    if(not output_name.endswith(".pdf")):
        output_name = output_name + ".pdf"
    
    merger.write(output_name)
    
    
def convert_to_pdf(paths: list)-> tuple:
    soffice = process.get_soffice_path()
    if not soffice:
        print("Fatal Error: LibreOffice 'soffice' not found on your system.\nVerify if it exists on your PATH.")
        sys.exit()

    # Filter out unsupported files (if not already done earlier)
    filtered_paths = []
    for item in paths:
        file = Path(item)
        if file.suffix.lower() in ALLOWED_FORMATS:
            filtered_paths.append(file)
        else:
            print(f"[rejected] `{item}`: not valid filetype")

    if not filtered_paths:
        print("No valid files to convert.")
        return False
    
    temp_dir = Path("./temp")
    temp_dir.mkdir(exist_ok=True)

    for input_path in filtered_paths:
        try:
            subprocess.run([
                soffice, "--headless", "--convert-to", "pdf",
                str(input_path), "--outdir", str(temp_dir)
            ], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error converting `{input_path}`: {e}")
            
    temp = []
    for item in filtered_paths:
        item = "./temp/"+str(item)
        temp.append(item)
        
    filtered_paths = temp
        
    return tuple(filtered_paths)
    

    