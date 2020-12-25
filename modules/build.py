import os
import modules.message
import json
import glob
import sass
import sys
from PIL import Image

def compileStyleSheets(LASTBUILD,file_format):
    modules.message.message(f"Stylesheet files format = {file_format}")
    stylesheet_files = glob.glob("./assets/stylesheets/**", recursive=True)
    for stylesheet_file in stylesheet_files:
        if os.path.splitext(stylesheet_file)[-1] == f".{file_format}":
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

def conversionImageToWebp(LASTBUILD):
    os.makedirs("./dist/images", exist_ok=True)
    modules.message.message("Conversion images to webp format...")
    images = glob.glob("./assets/images/**",recursive=True)
    images_format = [".bmp",".jpg",".jpeg",".png"]
    for image_file in images:
        if os.path.splitext(image_file)[-1].lower() in images_format:
            img = Image.open(image_file)
            img.save(f"./dist/images/{os.path.basename(image_file)}.webp", "WEBP")
            modules.message.success(f"{image_file} conversioned to webp")
    modules.message.success("All images conversioned to webp format")


def main():
    try:
        with open("sl.json", "r") as f:
            configuration = json.load(f)
        modules.message.success("Loaded configuration file.")
    except FileNotFoundError:
        modules.message.error("This is not the SpiderLog directory.")
        sys.exit()
    compileStyleSheets(0.0, configuration["stylesheets_file_format"])   
    conversionImageToWebp(0.0)