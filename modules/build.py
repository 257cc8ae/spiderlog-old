import os
import shutil
import json
import glob
import sass
import sys
import time
from PIL import Image
import markdown
from css_html_js_minify import html_minify, js_minify, css_minify
import modules.message
from jinja2 import Template, Environment, FileSystemLoader

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
        if os.path.splitext(image_file)[-1].lower() in images_format and isFileNewer(lastbuild, image_file):
            img = Image.open(image_file)
            if img.width > width:
                img = img.resize((width, int(width * img.height / img.width)))
            img.save(
                f"./dist/images/{os.path.basename(image_file)}", quality=quality)
            img.save(
                f"./dist/images/{os.path.basename(image_file)}.webp", quality=quality)
            modules.message.success(
                f"\033[1mimage compressor:  \033[0m{image_file} conversioned to webp")
        elif os.path.isfile(image_file) and isFileNewer(lastbuild, image_file):
            shutil.copy(image_file, "./dist/images")
            modules.message.success(
                f"\033[1mimage compressor:  \033[0m{image_file} is copy to ./dist/images")
    modules.message.success(
        "\033[1mimage compressor:  \033[0mImage weight reduction is now complete.")


def imageResizerForFavicon(img, size, output):
    new_img = img.resize((size, size))
    new_img.save(output)


def faviconGenerater(lastbuild, path):
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

def render(name,data={}):
    env = Environment(loader=FileSystemLoader('.'))
    env.globals['render'] = render
    template = env.get_template(f"./components/{name}.html.j2")
    return template.render(data)

def generateLayout():
    env = Environment(loader=FileSystemLoader('.'))
    env.globals['render'] = render
    template = env.get_template('./layouts/application.html.j2')
    data = {
        "lang": "ja",
        "title": "タイトル",
    }

    rendered = template.render(data)
    print(str(rendered))

def page_builder():
    pages = glob.glob("./pages/**", recursive=True)
    markdown_extensions = [".md",".markdown"]
    html_extensions = [".html",".htm"]
    md = markdown.Markdown()
    for page in pages:
        if os.path.isfile(page) and os.path.splitext(page)[-1] in markdown_extensions:
            dirname, basename = os.path.split(page)
            dirname = dirname.replace("./pages","")
            os.makedirs(f"./dist{dirname}",exist_ok=True)
            with open(page,"r") as markdown_file:
                with open(f"./dist{dirname}/{os.path.splitext(os.path.basename(page))[0]}.html","w") as parsed_html_file:
                    try:
                        parsed_html_file.write(html_minify(md.convert(markdown_file.read())))
                        modules.message.success(f"\033[1mpage builder:\033[0m Compiled {page}")
                    except SyntaxError:
                        modules.message.warn(f"\033[1mpage builder: \033[0mhtml syntax error")
                        parsed_html_file.write(md.convert(markdown_file.read()))
        elif os.path.isfile(page) and os.path.splitext(page)[-1] in html_extensions:
            dirname, basename = os.path.split(page)
            dirname = dirname.replace("./pages","")
            os.makedirs(f"./dist{dirname}",exist_ok=True)
            with open(page,"r") as html_file:
                with open(f"./dist{dirname}/{basename}","w") as parsed_html:
                    try:
                        parsed_html.write(html_minify(md.convert(html_file.read())))
                        modules.message.success(f"\033[1mpage builder:\033[0m Compiled {page}")
                    except SyntaxError:
                        modules.message.warn(f"\033[1mpage builder: \033[0mhtml syntax error")
                        parsed_html.write(md.convert(html_file.read()))

def javascriptCompile():
    js_files = glob.glob("./javascripts/**",recursive=True)
    for js_file in js_files:
        if os.path.isfile(js_file) and os.path.splitext(js_file)[-1] == ".js":
            dirname, basename = os.path.split(js_file)
            dirname = dirname.replace("./javascripts","")
            os.makedirs(f"./dist/js{dirname}",exist_ok=True)
            with open(js_file,"r") as javascript_file:
                with open(f"./dist/js{dirname}/{basename}", "w") as javascript_file_minified:
                    javascript_file_minified.write(js_minify(javascript_file.read()))
                    modules.message.success(f"\033[1mJavaScript Minify: \033[0mminified {js_file}")

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
    faviconGenerater(lastbuild, configuration["favicon_generater"]["path"])
    page_builder()
    javascriptCompile()
    generateLayout()
    with open(".lastbuild", "w") as f:
        f.write(str(time.time()))