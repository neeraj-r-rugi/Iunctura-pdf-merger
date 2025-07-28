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


#system Imports
import argparse
from pathlib import Path
import shutil

#Source files
import src.process as util
import src.files as files
import conversion as converter
import src.errors as error

def init_parser()->argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pdfMerger", description="A tool to merge or convert PDF's in a directory")
    parser.add_argument(
                        "--mode", "-m", 
                        choices=["merge", "conv", "convmerge"],
                        default="merge", 
                        help="The mode in which the directory is to be evaluated.\
                            \nmerge: Merge all files\nconv: Convert all files to pdf.\nconvmerge: Covert any non complaint files and merge.\nDefault: `merge`")
    parser.add_argument("--directory", "-dir", 
                        nargs= "+",
                        type=util.is_dir_valid,
                        default="./",
                        help="The Directory of the file(s) to be merged or converted\nDefault: `./` i.e. the `PWD`")
    parser.add_argument("--exclude", "-ex",
                        nargs="+",
                        type=util.is_valid_file,
                        default="",
                        help="File(s) to be excluded from operations\nDefault: `NULL`")
    parser.add_argument("--file", "-f",
                        nargs="+",
                        type=util.is_valid_file,
                        default="",
                        help="File(s) to be opertaed upon. Works on individual file rather than complete directory.\nDefault: `NULL`")
    parser.add_argument("--order", "-ord",
                        choices=["none","asec", "desc"],
                        default="none",
                        help="Choose weather the files are sorted in ascending(`asec`), desecnding(`desc`) order, or no order(system determined)(`none`).\nDefault: `none`.\
                        Note: The sorting is done on the filename and not on the names of the sub-directories.")
    parser.add_argument("--priority", "-pr",
                        choices=["file", "dir"],
                        default="dir",
                        help="Changes the priority, i.e. order weather the file flag is merged first or directory is merged first.\nDefault: `dir`")
    parser.add_argument("--walk", "-wl",
                        action='store_true',
                        default=False, 
                        help="Weather to walk through and perform actions on sub-directories present in given context.Flag is type boolean, presence is True.")
    parser.add_argument("--outputFile", "-of",
                        default="./pdfmc_merged.pdf",
                        type=util.enforce_pdf_path,
                        help=f"Name or path of the merged output file.Usage: `./[fileName].pdf`. Default: `./pdfmc_merged.pdf`.")
    parser.add_argument("--outputDir", "-od",
                        default="./temp/",
                        type=util.enforce_dir_path,
                        help="Name or path of the merged output directory(). Usage: `./[dirName]/`. Default: `./temp/`.")
    parser.add_argument("--showFiles", "-sf",
                        action= 'store_true',
                        default=False,
                        help="Shows all the files and the order in which the the files would be operated on. Does not perfrom any operation.")
    parser.add_argument("-keepDir", "-ke",
                        action="store_true",
                        default= False,
                        help="Weather to keep the temporary output directory used during convmerge operation.")
    
    return parser

def main() -> None:
    """
    Program execution begins here.
    """
    
    parser = init_parser()
    
    user_args = parser.parse_args()
    user_args = {"mode": user_args.mode, "dir":user_args.directory,"file":user_args.file ,
                 "execlude":user_args.exclude, "order":user_args.order, 
                 "priority":user_args.priority, "walk":user_args.walk, 
                 "outputFile":user_args.outputFile, "outputDir":user_args.outputDir,
                 "showFiles":user_args.showFiles, "keepDir":user_args.keepDir}
    try:
        if(user_args["dir"] == "" and user_args["file"] == ""):
            raise error.fileNotFoundError("No Files to Evaluate.")
    except Exception as e:
        print(e)
    
    #sort files provided via the `files` parameter
    try:
        if(user_args["order"] == "asec"):
            user_args["file"] = sorted(user_args["file"], key=lambda f: Path(f).name.lower())
        elif(user_args["order"] == "desc"):
            user_args["file"] = sorted(user_args["file"], key=lambda f: Path(f).name.lower(), reverse=True)
        else:
            pass
    except Exception as e:
        print(f"Failed to Order External Files: {e}")
    print(f"Beginning Operations....\n\n{"#"*50}")
    match(user_args["mode"]):
        case "merge":
            all_files = tuple(files.get_pdf_files(user_args["dir"], user_args["file"], 
                                                user_args["walk"], user_args["order"], 
                                                user_args["execlude"], user_args["priority"]))
            if(not user_args["showFiles"]):
                converter.save_as_pdf(all_files, user_args["outputFile"])
                if(all_files):
                    print(f"\n\nMerged Files: {all_files}\nIn that order.\n\n")
                else:
                    print("No Files to convert in the given context(s).")
            else:
                print(f"The files that will be processed are:\n{all_files}\nIn that order. With output file being stored in: {user_args['outputFile']}")
                
        case "conv":
            all_files = tuple(files.get_all_files(user_args["dir"], user_args["file"], 
                                                user_args["walk"], user_args["order"], 
                                                user_args["execlude"], user_args["priority"]))
            if(not user_args["showFiles"]):
                filtered_paths = converter.convert_to_pdf(all_files, user_args["outputDir"])
                print(f"Files saved: \n{filtered_paths} \nin dir: {user_args["outputDir"]}")
            else:
                print(f"The files that will be converted are: \n{all_files}. And would be stored in temporary directory: {user_args['outputDir']}")
        case "convmerge":
            all_files = files.get_all_files(user_args["dir"], user_args["file"], 
                                                user_args["walk"], user_args["order"], 
                                                user_args["execlude"], user_args["priority"])
            filtered_paths = converter.convert_to_pdf(all_files, user_args["outputDir"])
            all_files = files.merge_filtered_path(all_files, filtered_paths)
            pdf_files = [file for file in all_files if Path(file).suffix.lower() == ".pdf"]
            if(not user_args["showFiles"]):
                converter.save_as_pdf(pdf_files, user_args["outputFile"])
                print(f"\n\nMerged Files: {pdf_files}\nIn that order.\n\n")
                if(not user_args["keepDir"]):
                    shutil.rmtree(user_args["outputDir"])
            else:
                print(f"The Files that will be processed are\n: {pdf_files}\nIn that order.With File name: {user_args['outputFile']}, and Temporary directory being: {user_args["outputDir"]}")
                if(not user_args["keepDir"]):
                    shutil.rmtree(user_args["outputDir"])
                    print(f"Output directoty {user_args['outputDir']} removed.")
            
            
    print(f"Completed all Operations\n{"*"*50}")
             
            
            
            




if __name__ == "__main__":
    main()
