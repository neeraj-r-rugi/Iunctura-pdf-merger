

#system Imports
import argparse
from pathlib import Path
import shutil

#Source files
import src.process as util
import src.files as files
import src.conersion as converter

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
                        default="temp/",
                        type=util.enforce_dir_path,
                        help="Name or path of the merged output directory(). Usage: `./[dirName]/`. Default: `./temp/`.")
    
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
                 "outputFile":user_args.outputFile, "outputDir":user_args.outputDir}
    
    if(user_args["dir"] == "" and user_args["file"] == ""):
        print(f"No Files to Process\nProgram Terminated\n{"*"*50}")
        return
    
    #sort files provided via the `files` parameter
    if(user_args["order"] == "asec"):
        user_args["file"] = sorted(user_args["file"], key=lambda f: Path(f).name.lower())
    elif(user_args["order"] == "desc"):
        user_args["file"] = sorted(user_args["file"], key=lambda f: Path(f).name.lower(), reverse=True)
    else:
        pass
        
    print("Beginning Operations....\n")
    match(user_args["mode"]):
        case "merge":
            all_files = tuple(files.get_pdf_files(user_args["dir"], user_args["file"], 
                                            user_args["walk"], user_args["order"], 
                                            user_args["execlude"], user_args["priority"]))
            converter.save_as_pdf(all_files, user_args["outputFile"])
            print(f"\n\nMerged Files: {all_files}\nin that order.\n\n") 
            
        case "conv":
            all_files = tuple(files.get_all_files(user_args["dir"], user_args["file"], 
                                            user_args["walk"], user_args["order"], 
                                            user_args["execlude"], user_args["priority"]))
            filtered_paths = converter.convert_to_pdf(all_files, user_args["outputDir"])
            print(f"Files saved: \n{filtered_paths} \nin dir: {user_args["outputDir"]}")
        case "convmerge":
            all_files = files.get_all_files(user_args["dir"], user_args["file"], 
                                            user_args["walk"], user_args["order"], 
                                            user_args["execlude"], user_args["priority"])
            filtered_paths = converter.convert_to_pdf(all_files, user_args["outputDir"])
            all_files = files.merge_filtered_path(all_files, filtered_paths)
            converter.save_as_pdf(all_files, user_args["outputFile"])
            print(f"\n\nMerged Files: {all_files}\nin that order.\n\n")
            shutil.rmtree(user_args["outputDir"])
            
            
    print(f"Completed all Operations\n{"*"*50}")
             
            
            
            




if __name__ == "__main__":
    main()