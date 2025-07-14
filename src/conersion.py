import pypdf as pdf
import os
import process
from pathlib import Path
import subprocess

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
    
    # Already-PDF (sometimes used for reprocessing)
    ".pdf",
]

def save_pdf(paths: list, output_name:str):
    merger = pdf.PdfWriter()
    for file in paths:
        merger.append(str(file))
    
    if(not output_name.endswith(".pdf")):
        output_name = output_name + ".pdf"
    
    merger.write(output_name)
    
    
def convert_to_pdf(paths: list):
    soffice = process.get_soffice_path()
    if not soffice:
        print("Fatal Error: LibreOffice 'soffice' not found on your system.\nVerify if it exists on your PATH.")
        return False
    
    for item in paths:
        file = Path(item)
        if(not file.suffix.lower() in ALLOWED_FORMATS):
            paths.remove(item)
    
    
    temp_dir = Path("./temp")
    temp_dir.mkdir()
    for file in paths:
        input_path = Path(file)
    

    