import os
import shutil
import json
import glob
import sass
import sys
import time
from PIL import Image
import modules.message


def isFileNewer(lastbuild, path):
    if os.stat(path).st_mtime >= lastbuild:
        return True
    else:
        return False

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


def imageCompressor(lastbuild, width, quality):
    if quality > 95:
        modules.message.warn(
            "\033[1mimage compressor:  \033[0mA quality value greater than 95 is not recommended.")
    os.makedirs("./dist/images", exist_ok=True)
    modules.message.message("Conversion images to webp format...")
    images = glob.glob("./assets/images/**", recursive=True)
    images_format = [".bmp", ".jpg", ".jpeg", ".png"]
    for image_file in images:
        if os.path.splitext(image_file)[-1].lower() in images_format and isFileNewer(lastbuild,image_file):
            img = Image.open(image_file)
            if img.width > width:
                img = img.resize((width, int(width * img.height / img.width)))
            img.save(
                f"./dist/images/{os.path.basename(image_file)}", quality=quality)
            img.save(
                f"./dist/images/{os.path.basename(image_file)}.webp", quality=quality)
            modules.message.success(
                f"\033[1mimage compressor:  \033[0m{image_file} conversioned to webp")
        elif os.path.isfile(image_file) and isFileNewer(lastbuild,image_file):
            shutil.copy(image_file, "./dist/images")
            modules.message.success(
                f"\033[1mimage compressor:  \033[0m{image_file} is copy to ./dist/images")
    modules.message.success(
        "\033[1mimage compressor:  \033[0mImage weight reduction is now complete.")


def imageResizerForFavicon(img, size, output):
    new_img = img.resize((size, size))
    new_img.save(output)


def faviconGenerater(lastbuild):
    path = "./static/favicon.png"
    output_favicon_images = {
        "android-chrome-192x192.png": 192,
        "android-chrome-384x384.png": 384,
        "apple-touch-icon.png": 180,
        "favicon.ico": 48,
        "favicon-32x32.png": 32,
        "mstile-150x150.png": 150,
    }
    if os.path.isfile(path) and isFileNewer(lastbuild, path):
        print(os.stat(path).st_mtime)
        img = Image.open(path)
        if img.width == img.height and img.width >= 260:
            for favicon_image_file_name in output_favicon_images:
                imageResizerForFavicon(
                    img, output_favicon_images[favicon_image_file_name], f"./dist/{favicon_image_file_name}")
                modules.message.success(
                    f"\033[1mfavicon generater: \033[0m{favicon_image_file_name} is compiled.")
        elif img.width != img.height:
            modules.message.warn(
                "\033[1mfavicon generater: \033[0mfavicon.png's ratio is recommendation 1:1.")
        elif img.width >= 260:
            modules.message.warn(
                "\033[1mfavicon generater: \033[0mYour image should be 260x260 or more for optimal results.")
    elif os.path.isfile(path) == False:
        modules.message.warn(
            f"\033[1mfavicon generater: \033[0mNot found {path}")


def main():
    with open(".lastbuild", "r") as f:
        lastbuild = float(f.read())
    try:
        with open("sl.json", "r") as f:
            configuration = json.load(f)
        modules.message.success("Loaded configuration file.")
    except FileNotFoundError:
        modules.message.error("This is not the SpiderLog directory.")
        sys.exit()
    compileStyleSheets(lastbuild, configuration["stylesheets_file_format"])
    imageCompressor(lastbuild, configuration["image_compressor"]
                    ["width"], configuration["image_compressor"]["quality"])
    faviconGenerater(lastbuild)
    with open(".lastbuild", "w") as f:
        f.write(str(time.time()))
