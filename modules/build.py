import os
import shutil
import json
import glob
import sass
import sys
from PIL import Image
import modules.message


def compileStyleSheets(LASTBUILD, file_format):
    modules.message.message(f"Stylesheet files format = {file_format}")
    stylesheet_files = glob.glob("./assets/stylesheets/**", recursive=True)
    for stylesheet_file in stylesheet_files:
        if os.path.splitext(stylesheet_file)[-1] == f".{file_format}":
            new_css_file_path = stylesheet_file.replace(
                "./assets/stylesheets", "")
            if new_css_file_path.count("/") >= 2:
                os.makedirs(
                    f"./dist/stylesheets{os.path.dirname(new_css_file_path)}", exist_ok=True)
                output_css_path = f"./dist/stylesheets{os.path.dirname(new_css_file_path)}/{os.path.splitext(os.path.basename(new_css_file_path))[0]}.css"
            else:
                output_css_path = f"./dist/stylesheets/{os.path.splitext(os.path.basename(new_css_file_path))[0]}.css"
            try:
                with open(stylesheet_file, "r") as stylesheet:
                    scss_compiled_code = sass.compile(
                        string=stylesheet.read(), output_style='compressed')
                    with open(output_css_path, "w") as compiled_css:
                        compiled_css.write(scss_compiled_code)
                        modules.message.success(
                            f"{stylesheet_file} is compiled.")
            except sass.CompileError as e:
                modules.message.error(f"{file_format} copmile error")
                print(e)


def conversionImageToWebp(LASTBUILD):
    os.makedirs("./dist/images", exist_ok=True)
    modules.message.message("Conversion images to webp format...")
    images = glob.glob("./assets/images/**", recursive=True)
    images_format = [".bmp", ".jpg", ".jpeg", ".png"]
    for image_file in images:
        if os.path.splitext(image_file)[-1].lower() in images_format:
            img = Image.open(image_file)
            if img.width > 800:
                img = img.resize((800, int(800 * img.height / img.width)))
            img.save(
                f"./dist/images/{os.path.basename(image_file)}", quality=60)
            img.save(
                f"./dist/images/{os.path.basename(image_file)}.webp", quality=60)
            modules.message.success(f"{image_file} conversioned to webp")
        elif os.path.isfile(image_file):
            shutil.copy(image_file, "./dist/images")
            modules.message.success(f"{image_file} is copy to ./dist/images")
    modules.message.success("All images conversioned to webp format")

def imageResizerForFavicon(img,size,output):
    new_img = img.resize((size,size))
    new_img.save(output)

def faviconGenerater():
    output_favicon_images = {
        "android-chrome-192x192.png": 192,
        "android-chrome-384x384.png": 384,
        "apple-touch-icon.png": 180,
        "favicon.ico": 48,
        "favicon-32x32.png": 32,
        "mstile-150x150.png": 150,
    }
    if os.path.isfile("./static/favicon.png"):
        img = Image.open("./static/favicon.png")
        if img.width == img.height and img.width >= 260:
            for favicon_image_file_name in output_favicon_images:
                imageResizerForFavicon(img,output_favicon_images[favicon_image_file_name],f"./dist/{favicon_image_file_name}")
                modules.message.success(f"\033[1mfavicon generater: \033[0m{favicon_image_file_name} is compiled.")
        elif img.width != img.height:
            modules.message.warn("\033[1mfavicon generater: \033[0mfavicon.png's ratio is recommendation 1:1.")
        elif img.width >= 260:
            modules.message.warn("\033[1mfavicon generater: \033[0mYour image should be 260x260 or more for optimal results.")
    else:
        modules.message.warn("\033[1mfavicon generater: \033[0mNot found ./static/favicon.png")

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
    faviconGenerater()
