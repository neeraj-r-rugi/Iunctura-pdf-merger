

#system Imports
import argparse

#Source files
import src.process as util
import src.files as files
import src.conersion as converter

def main() -> None:
    """
    Program execution begins here.
    """
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
                        choices=["asec", "desc"],
                        default="asc",
                        help="Choose weather the files are sorted in ascending(`asec`) or desecnding(`desc`) order.\nDefault: `asec`")
    parser.add_argument("--priority", "-pr",
                        choices=["file", "dir"],
                        default="dir",
                        help="Changes the priority, i.e. order weather the file flag is merged first or directory is merged first.\nDefault: `dir`")
    parser.add_argument("--walk", "-wl",
                        action='store_true',
                        default=False, 
                        help="Weather to walk through and perform actions on sub-directories present in given context.Flag is type boolean, presence is True.")
    parser.add_argument("--output", "-o",
                        default="./pdfmc_merged.pdf",
                        help="Name or path of the merged output file. Default: `./pdfmc_merged.pdf`.")
    
    
    user_args = parser.parse_args()
    user_args = {"mode": user_args.mode, "dir":user_args.directory,"file":user_args.file ,
                 "execlude":user_args.exclude, "order":user_args.order, 
                 "priority":user_args.priority, "walk":user_args.walk, "output":user_args.output}
    
    if(user_args["order"] == "asec"):
        user_args["file"] = sorted(user_args["file"])
    else:
        user_args["file"] = sorted(user_args["file"], reverse=True)
        
    match(user_args["mode"]):
        case "merge":
            all_files = files.get_pdf_files(user_args["dir"], user_args["file"], 
                                            user_args["walk"], user_args["order"], 
                                            user_args["execlude"])
            converter.save_pdf(all_files, user_args["output"]) 
            
        case "conv":
            all_files = files.get_all_files(user_args["dir"], user_args["file"], 
                                            user_args["walk"], user_args["order"], 
                                            user_args["execlude"])
            converter.convert_to_pdf(all_files)
        case "convmerge":
            pass




if __name__ == "__main__":
    main()