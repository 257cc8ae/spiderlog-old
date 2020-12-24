import os
import modules.message
def main():
    # try:
    #     with open("spiderlog.yml", "r") as f:
    #         pass
    #     print("fuck")
    # except FileNotFoundError:
    #     modules.message.error("This directory is not the SpiderLog directory.")
    if os.path.isfile("spiderlog.yml"):
        print("google")
    # # Read .LASTBUILD file
    # if os.path.exists(".LASTBUILD"):
    #     with open(".LASTBUILD") as f:
    #         LASTBUILD = float(f.read())
    # else:
    #     LASTBUILD = 0.0
    # # Compile SCSS files
    # os.makedirs("./dist/stylesheets", exist_ok=True)
    # files = glob.glob("./assets/stylesheets/**", recursive=True)
    # re_scss_file_path = re.compile(r".\/assets\/stylesheets\/.*.scss")
    # for scss_file in files:
    #     if re_scss_file_path.fullmatch(scss_file) and LASTBUILD <= os.stat(scss_file).st_mtime:
    #         with open(scss_file, "r") as f:
    #             NEW_CSS_FILE_PATH = scss_file.replace(
    #                 "./assets/stylesheets", "")
    #             if NEW_CSS_FILE_PATH.count("/") >= 2:
    #                 os.makedirs(
    #                     f"./dist/stylesheets{os.path.dirname(NEW_CSS_FILE_PATH)}", exist_ok=True)
    #             try:
    #                 css_code = sass.compile(
    #                     string=f.read(), output_style='compressed')
    #                 with open(f"./dist/stylesheets{NEW_CSS_FILE_PATH[:-5]}.css", "w") as css_file:
    #                     css_file.write(css_code)
    #                 success(f"{scss_file} is compiled.")
    #             except sass.CompileError:
    #                 with open(f"./dist/stylesheets{NEW_CSS_FILE_PATH[:-5]}.css", "w") as css_file:
    #                     css_file.write("")
    #                 warn(
    #                     f"There was a problem with the compilation of SCSS.")
    #                 success(f"{scss_file} is compiled.")

    # # Make .LASTBUILD file
    # with open(".LASTBUILD", "w") as f:
    #     f.write(str(time.time()))