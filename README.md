# IuncturaPdfMerger 
Tired of having to manually convert and merge your lecture slides? Well fear not as Iunctura Is here to save the day!

## What is Iunctura?
It is a comprehensive tool to merge and convert PDF files in directories with flexible options for file handling and organization.

## Overview

Iunctura is a command-line utility that can:
- Merge multiple PDF files into a single document
- Convert non-PDF files to PDF format
- Combine conversion and merging operations
- Process files from specific directories or individual files
- Handle subdirectories recursively

## Basic Usage
Note: All Examples shown on Linux Machine.

### Running with Python
```bash
python3 main.py [options]
```

### Using the Binary (Recommended)
For easier usage, you can use the provided binary or create your own:

**Using the provided binary:**
```bash
# If binary is in your PATH
iunctura [options]

# If binary is in current directory
./iunctura [options]
```

**Creating your own binary with PyInstaller:**
```bash
# Install PyInstaller
pip install pyinstaller

# Create binary
pyinstaller --onefile main.py --name iunctura

# Move to system PATH (Linux/Mac)
sudo mv dist/iunctura /usr/local/bin/

# Or add to PATH (Windows)
# Move iunctura.exe to a directory in your PATH
```

Once the binary is in your system PATH, you can use `iunctura` from anywhere on your system.

## Command Line Arguments

### Mode Selection (`--mode`, `-m`)

Controls the primary operation mode:

- **`merge`** (default): Merge all PDF files in the specified location
- **`conv`**: Convert all non-PDF files to PDF format
- **`convmerge`**: Convert any non-PDF files to PDF and then merge all the specified files

```bash
# Merge existing PDFs only
python3 main.py --mode merge
# or with binary
iunctura --mode merge

# Convert files to PDF
python3 main.py -m conv
# or with binary
iunctura -m conv

# Convert and merge in one operation
python3 main.py -m convmerge
# or with binary
iunctura -m convmerge
```

### Directory Selection (`--directory`, `-dir`)

Specify one or more directories to process. Accepts multiple directory paths.

```bash
# Process current directory (default)
python3 main.py
# or with binary
iunctura

# Process specific directory
python3 main.py --directory /path/to/pdfs/
# or with binary
iunctura --directory /path/to/pdfs/

# Process multiple directories
python3 main.py -dir ./docs/ ./reports/ ./archives/
# or with binary
iunctura -dir ./docs/ ./reports/ ./archives/
```

### File Exclusion (`--exclude`, `-ex`)

Exclude specific files from processing. Useful when you want to process a directory but skip certain files. Performs checks based of file name, if two files of same name in different directories are present, both will be excluded.

```bash
# Exclude single file
python3 main.py --exclude document1.pdf

# Exclude multiple files
python3 main.py -ex file1.pdf file2.docx unwanted.txt
```

### Individual File Processing (`--file`, `-f`)

Used to combine specific files with entire directories or process individual files.
Note: It does not override directory file processing, it just adds on to the directory files. Unless explicitly stated by setting dir parameter to `""`.

```bash
# Process specific files
python3 main.py --directory "" --file document1.pdf document2.pdf

# Mix different file types (useful with conv mode)
python3 main.py -d "" -f report.docx presentation.pptx -m convmerge

#Add extra files to process with files in a directory
python3 main.py -d "./my_dir/" -f "./other_dir/test.pdf" "./other_dir/test2.pdf"
```

### File Ordering (`--order`, `-ord`)

Control the order in which files are processed during merging:

- **`none`** (default): System-determined order
- **`asec`**: Ascending order by filename
- **`desc`**: Descending order by filename

```bash
# Alphabetical order (A to Z)
python3 main.py --order asec

# Reverse alphabetical order (Z to A)
python3 main.py -ord desc
```

### Processing Priority (`--priority`, `-pr`)

When both `--file` and `--directory` are specified, this determines processing and final PDF order. Useful if you want your specified files to be present in the beginning of the combined PDF:

- **`dir`** (default): Process directory files first, then individual files
- **`file`**: Process individual files first, then directory files

```bash
# Process individual files before directory files
python3 main.py --file important.pdf -dir ./docs/ --priority file
```

### Recursive Directory Processing (`--walk`, `-wl`)

Enable recursive processing of subdirectories. This is a boolean flag.

```bash
# Process subdirectories recursively
python3 main.py --walk

# Short form
python3 main.py -wl
```

### Output File (`--outputFile`, `-of`)

Specify the name and path for the merged output PDF file.

```bash
# Custom output file
python3 main.py --outputFile ./merged_documents.pdf

# Output to different directory
python3 main.py -of /path/to/output/final_merge.pdf
```

### Output Directory (`--outputDir`, `-od`)

Specify the directory for temporary files and conversion outputs.

```bash
# Custom output directory
python3 main.py --outputDir ./conversion_temp/

# Different temp location
python3 main.py -od /tmp/pdfmerger_work/
```

### Show Files Preview (`--showFiles`, `-sf`)

Display all files and the order in which they would be processed without performing any actual operations. This is useful for testing and verification.

```bash
# Preview files that would be processed
python3 main.py --showFiles

# Preview with specific settings
python3 main.py -sf --directory ./docs/ --order asec --walk
```

### Keep Temporary Directory (`--keepDir`, `-ke`)

Preserve the temporary output directory used during conversion and merge operations instead of cleaning it up automatically.

```bash
# Keep temporary files after processing
python3 main.py --keepDir

# Useful for debugging conversion issues
python3 main.py -ke --mode convmerge --outputDir ./debug_temp/
```

## Common Use Cases

### Basic PDF Merge

Merge all PDFs in the current directory:

```bash
python3 main.py
# or with binary
iunctura
```

### Merge with Custom Output

Merge PDFs with a specific output filename:

```bash
python3 main.py --outputFile ./monthly_reports.pdf
# or with binary
iunctura --outputFile ./monthly_reports.pdf
```

### Convert and Merge Mixed Files

Convert Word documents and PowerPoint files to PDF, then merge with existing PDFs:

```bash
python3 main.py --mode convmerge --directory ./mixed_docs/
```

### Process Specific Files Only

Merge only selected files in a specific order:

```bash
python3 main.py --directory "" --file cover.pdf intro.pdf chapter1.pdf chapter2.pdf --order asec
```

### Recursive Directory Processing

Process all PDFs in a directory tree, excluding certain files:

```bash
python3 main.py --walk --exclude draft.pdf temp.pdf --outputFile ./complete_archive.pdf
```

### Complex Multi-Directory Operation

Process multiple directories recursively, convert non-PDFs, and merge everything:

```bash
python3 main.py \
    --mode convmerge \
    --directory ./reports/ ./presentations/ ./documents/ \
    --walk \
    --exclude template.docx \
    --order asec \
    --outputFile ./comprehensive_merge.pdf \
    --outputDir ./temp_conversion/
```

### Preview Before Processing

Check which files would be processed and in what order:

```bash
python3 main.py --showFiles --directory ./reports/ --order asec
```

### Debug Conversion Issues

Keep temporary files to troubleshoot conversion problems:

```bash
python3 main.py --mode convmerge --keepDir --outputDir ./debug_temp/
```

## File Type Support

- **PDF files**: Directly merged (merge mode)
- **Non-PDF files**: Converted to PDF first (conv and convmerge modes)
- Common supported formats typically include: .docx, .pptx, .txt, .jpg, .png (depends on conversion utilities)

## Tips and Best Practices

1. **File Naming**: Use descriptive names for output files to avoid confusion
2. **Directory Structure**: Organize files logically before processing for better results
3. **Exclusions**: Use `--exclude` to skip temporary files, templates, or work-in-progress documents
4. **Testing**: Run with `--showFiles` first to verify file selection and order before processing
5. **Backup**: Always backup original files before processing, especially with conversion operations
6. **Order Matters**: Use `--order` when the sequence of merged content is important. Using `none` leaves it to the mercy of your computers filesystem.
7. **Debugging**: Use `--keepDir` to preserve temporary files when troubleshooting conversion issues
8. **Binary Usage**: For convenience, use the provided binary or create your own with PyInstaller and add it to your system PATH

## Default Behavior

When run without arguments, pdfMerger will:
- Use merge mode
- Process the current directory
- Use system-determined file order
- Prioritize directory processing over individual files
- Not walk subdirectories
- Not show files preview
- Not keep temporary directories
- Output to `./pdfmc_merged.pdf`
- Use `./temp/` as the temporary directory

## Error Handling

The program includes validation for:
- Directory existence and accessibility
- File path validity
- PDF extension enforcement for output files
- Directory path formatting for output directories

Make sure all specified paths exist and are accessible before running the program.

## ⚙️ Some Points to Note:

- 📝 **PDF Conversion Requires LibreOffice**  
  While this tool can merge PDF files out of the box, converting other file types (such as `.docx`, `.odt`, `.txt`, etc.) to PDF requires the **LibreOffice suite** to be installed on your system.  
  The tool uses the `soffice` command in **headless mode** via `subprocess`.  
  - Ensure `libreoffice` or `soffice` is in your system's `PATH`.
  - Uses: `soffice --headless --convert-to pdf <input-file> --outdir <output-dir>`
  - To install using apt: `sudo apt install libreoffice` for windows intall from the official LibreOffice Website!

- 🔢 **Ordering Merged Files**  
  To merge files in a specific order from a directory, it's recommended to **prefix filenames with numbers**.  
  Example: `1_intro.pdf`, `2_chapter.pdf`, `3_summary.pdf`  
  Then, use the `--order` parameter to maintain this sequence during the merge.

- 💻 **Use UNIX-style Paths (Even on Windows)**  
  Prefer **Unix-style paths with forward slashes (`/`)** for better cross-platform compatibility, even on Windows.  
  Example:  
  ✅ `C:/Users/Me/Documents/file.pdf`  
  ❌ `C:\Users\Me\Documents\file.pdf`  
  While type checking and normalization are handled internally, using consistent formatting reduces errors and improves reliability. All paths/filenames entered must be either relative path with respect to the terminal context, or the absolute path of the file.