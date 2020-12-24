import os
import modules.message
import json
import glob
import sass
import sys

def compileStyleSheets(LASTBUILD,file_format):
    modules.message.message(f"Stylesheet files format = {file_format}")
    stylesheet_files = glob.glob("./assets/stylesheets/**", recursive=True)
    for stylesheet_file in stylesheet_files:
        if os.path.splitext(stylesheet_file)[1] == f".{file_format}":
            new_css_file_path = stylesheet_file.replace("./assets/stylesheets","")
            if new_css_file_path.count("/") >= 2:
                os.makedirs(f"./dist/stylesheets{os.path.dirname(new_css_file_path)}", exist_ok=True)
                output_css_path = f"./dist/stylesheets{os.path.dirname(new_css_file_path)}/{os.path.splitext(os.path.basename(new_css_file_path))[0]}.css"
            else:
                output_css_path = f"./dist/stylesheets/{os.path.splitext(os.path.basename(new_css_file_path))[0]}.css"
            try:
                with open(stylesheet_file, "r") as stylesheet:
                    scss_compiled_code = sass.compile(string=stylesheet.read(), output_style='compressed')
                    with open(output_css_path, "w") as compiled_css:
                        compiled_css.write(scss_compiled_code)
                        modules.message.success(f"{stylesheet_file} is compiled.")
            except sass.CompileError as e:
                modules.message.error(f"{file_format} copmile error")
                print(e)
                # NEW_CSS_FILE_PATH = stylesheet_file.replace(
                #     "./assets/stylesheets", "")
                # if NEW_CSS_FILE_PATH.count("/") >= 2:
                #     os.makedirs(
                #         f"./dist/stylesheets{os.path.dirname(NEW_CSS_FILE_PATH)}", exist_ok=True)
                # try:
                #     css_code = sass.compile(
                #         string=f.read(), output_style='compressed')
                #     with open(f"./dist/stylesheets{NEW_CSS_FILE_PATH[:-5]}.css", "w") as css_file:
                #         css_file.write(css_code)
                # except sass.CompileError:
                #     with open(f"./dist/stylesheets{NEW_CSS_FILE_PATH[:-5]}.css", "w") as css_file:
                #         css_file.write("")
                #     modules.message.warn(
                #         f"There was a problem with the compilation of SCSS.")
                #     modules.message.success(f"{stylesheet_file} is compiled.")

def main():
    try:
        with open("sl.json", "r") as f:
            configuration = json.load(f)
        modules.message.success("Loaded configuration file.")
    except FileNotFoundError:
        modules.message.error("This is not the SpiderLog directory.")
        sys.exit()
    compileStyleSheets(0.0, configuration["stylesheets_file_format"])   