import sys
import glob
import re
import sass
import os
import time
import modules.new


def error(text):
    print(f"\033[31m\033[1mERROR\033[0m {text}")


def success(text):
    print(f"\033[32m\033[1mSUCCESS\033[0m {text}")


def warn(text):
    print(f"\033[33m\033[1mWARN\033[0m {text}")


# def build():
#     # Read .LASTBUILD file
#     if os.path.exists(".LASTBUILD"):
#         with open(".LASTBUILD") as f:
#             LASTBUILD = float(f.read())
#     else:
#         LASTBUILD = 0.0
#     # Compile SCSS files
#     os.makedirs("./dist/stylesheets", exist_ok=True)
#     files = glob.glob("./assets/stylesheets/**", recursive=True)
#     re_scss_file_path = re.compile(r".\/assets\/stylesheets\/.*.scss")
#     for scss_file in files:
#         if re_scss_file_path.fullmatch(scss_file) and LASTBUILD <= os.stat(scss_file).st_mtime:
#             with open(scss_file, "r") as f:
#                 NEW_CSS_FILE_PATH = scss_file.replace(
#                     "./assets/stylesheets", "")
#                 if NEW_CSS_FILE_PATH.count("/") >= 2:
#                     os.makedirs(
#                         f"./dist/stylesheets{os.path.dirname(NEW_CSS_FILE_PATH)}", exist_ok=True)
#                 try:
#                     css_code = sass.compile(
#                         string=f.read(), output_style='compressed')
#                     with open(f"./dist/stylesheets{NEW_CSS_FILE_PATH[:-5]}.css", "w") as css_file:
#                         css_file.write(css_code)
#                     success(f"{scss_file} is compiled.")
#                 except sass.CompileError:
#                     with open(f"./dist/stylesheets{NEW_CSS_FILE_PATH[:-5]}.css", "w") as css_file:
#                         css_file.write("")
#                     warn(
#                         f"There was a problem with the compilation of SCSS.")
#                     success(f"{scss_file} is compiled.")

#     # Make .LASTBUILD file
#     with open(".LASTBUILD", "w") as f:
#         f.write(str(time.time()))

def main():
    PROCESS_NAME: str = sys.argv[1]
    if PROCESS_NAME == "new":
        modules.new.main()
    else:
        error(f"Could not find PROCESS NAME \"{PROCESS_NAME}\"")


if __name__ == "__main__":
    main()