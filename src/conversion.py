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
import pypdf as pdf
import os
from . import process
from pathlib import Path
import subprocess
import sys
from . import errors as error

ALLOWED_FORMATS = [
    # Text Documents
    ".doc", ".docx", ".odt", ".rtf", ".txt", ".fodt", ".html", ".htm",
    
    # Spreadsheets
    ".xls", ".xlsx", ".ods", ".csv", ".fods",
    
    # Presentations
    ".ppt", ".pptx", ".odp", ".fodp", ".pps", ".ppsx",
    
    # Drawings
    ".odg", ".fodg", ".svg", ".emf", ".wmf",
    
    # Other Office Formats
    ".xml", ".xhtml", ".epub",
]

#Overlaps do exist between Pandoc and Soffice, But Overlapped files are always handled by Soffice
PANDOC_FORMATS = [
    ".md", ".markdown", ".mdown", ".mkd", ".mkdn",
    ".rst", ".html", ".htm", ".tex", ".latex",
    ".ipynb", ".docx", ".odt", ".epub", ".fb2",
    ".docbook", ".xml", ".json", ".bib", ".bibtex",
    ".csljson", ".cslyaml", ".csv", ".tsv", ".opml",
    ".org", ".textile", ".t2t", ".mediawiki", ".muse",
    ".tikiwiki", ".twiki", ".vimwiki", ".jira", ".man",
    ".ms", ".tei", ".texi", ".plain", ".pptx",
    ".s5", ".slidy", ".slideous", ".revealjs", ".rtf"
]

def save_as_pdf(files: list, output_name:str):
    if(files):
        merger = pdf.PdfWriter()
        for file in files:
            merger.append(str(file))
            
        merger.write(output_name)
    
    
def convert_to_pdf(paths: list, output_dir: str)-> tuple:
    soffice = process.get_soffice_path()
    pandoc = process.get_pandoc_path()
    if not soffice:
        raise error.sofficeNotPresentError("Fatal Error: LibreOffice 'soffice' not found on your system.\nVerify if it exists on your PATH.")

    filtered_paths = []
    for item in paths:
        file = Path(item)
        if file.suffix.lower() in (ALLOWED_FORMATS+PANDOC_FORMATS):
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
    print(f"Output for Conversion of files to PDF from LibreOffice and/Or Pandoc:\n{"#"*50}")
    for input_path in filtered_paths:
        try:
            if input_path.suffix.lower() in ALLOWED_FORMATS:
                subprocess.run([
                    soffice, "--headless", "--convert-to", "pdf",
                    str(input_path), "--outdir", str(temp_dir)
                ], check=True)
                print(f"-------> [Converted] {input_path} to PDF\n{"*"*75}")
            else:
                subprocess.run([
                    pandoc, str(input_path), "--output", (str(temp_dir)+'/'+str(input_path.stem)+".pdf"), '--pdf-engine=wkhtmltopdf'
                ], check=True)
                print(f"-------> [Converted] {input_path} to PDF\n{"*"*75}")
        except subprocess.CalledProcessError as e:
            print(f"Error converting `{input_path}`: {e}")
            raise error.failedToConvertToPDFError(f"Conversion Failure")  
            
    temp = []
    
    for item in filtered_paths:
        item:Path = item.with_suffix(".pdf")
        item = f"{output_dir}"+str(Path(item).name)
        temp.append(item)
        
    filtered_paths = temp
    print(f"{"#"*50}")
    return filtered_paths
    

    