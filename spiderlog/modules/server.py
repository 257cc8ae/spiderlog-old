from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import os
import sys
import json
import re
import sass
import mimetypes
from PIL import Image
import io
from jinja2 import Template, Environment, FileSystemLoader
from spiderlog.modules import spiderMark
from spiderlog.modules import message
from spiderlog.modules import build

def loadSpiderLogConfigFile():
    try:
        with open("sl.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        message.error("This is not the SpiderLog directory.")
        sys.exit()


def isBinaryOrText(mimetype):
    mimetype_type = mimetype.split("/")[0]
    if mimetype_type == "text" or mimetype_type == "application" or mimetype == "image/svg+xml":
        return True
    else:
        return False


class SpiderServer(BaseHTTPRequestHandler):
    def do_GET(self):
        config = loadSpiderLogConfigFile()
        pageSettings = build.loadPagesSetting()
        path = self.path
        if path == "/":
            path = "/index.html"
        re_images_dir = re.compile(r"^\/images\/.*")
        path_ext = os.path.splitext(path)[-1]
        content_type = mimetypes.guess_type(path)[0]
        if content_type == None and path_ext == ".webp":
            content_type = "image/webp"
        request_status = 200
        response_body = ""
        if isBinaryOrText(content_type):
            if path_ext == ".css":
                path = path[:-3] + config["stylesheets_file_format"]
                try:
                    with open(f".{path}", "r") as f:
                        response_body = sass.compile(
                            string=f.read(), output_style='expanded')
                except FileNotFoundError:
                    request_status = 404
            elif path_ext == ".html":
                dirname, basename = os.path.split(path)
                basename = os.path.splitext(os.path.basename(basename))[0]
                page_file_formats = ['.htm', '.html', '.markdown', '.md']
                is_file_being = list()
                for page_file_format in page_file_formats:
                    if os.path.isfile(f"./pages{dirname + basename + page_file_format}"):
                        is_file_being.append(True)
                    else:
                        is_file_being.append(False)
                if is_file_being.count(True) == 0:
                    request_status = 404
                else:
                    page_file_format = page_file_formats[is_file_being.index(
                        True)]
                    pageSetting = build.makeCustomPageSetting(
                        (dirname + basename)[1:], pageSettings)
                    with open(f"./pages{dirname + basename + page_file_format}", "r") as f:
                        if mimetypes.guess_type(basename + page_file_format)[0] == "text/markdown":
                            pageSetting["yield"] = spiderMark.html(f.read())
                        elif mimetypes.guess_type(basename + page_file_format)[0] == "text/html":
                            pageSetting["yield"] = f.read()
                    pageSetting["headBuilder"] = build.headBuilder(pageSetting)
                    env = Environment(loader=FileSystemLoader('.'))
                    env.globals['render'] = build.render
                    template = env.get_template(
                        f"./layouts/{pageSetting['layout']}.html.j2")
                    rendered = template.render(pageSetting)
                    response_body = rendered
            elif path_ext == ".js":
                try:
                    with open("." + path , "r") as f:
                        response_body = f.read() 
                except FileNotFoundError:
                    request_status = 404
            elif path_ext == ".svg":
                if re_images_dir.match(path):
                    path = "." + path
                else:
                    path = f"./static{path}" 
                try:
                    with open(path, "r") as f:
                        response_body = f.read()
                except FileNotFoundError:
                    request_status = 404          
            else:
                try:
                    with open(f"./static{path}", "r") as f:
                        response_body = f.read()
                except FileNotFoundError:
                    request_status = 404

            self.send_response(request_status)
            self.send_header("Content-type", content_type)
            self.end_headers()
            self.wfile.write(bytes(response_body, "utf-8"))
        else:
            is_images_dir = False
            if re_images_dir.match(path):
                path = "." + path
                is_images_dir = True
            else:
                path = f"./static{path}"
            try:
                img = Image.open(path,mode="r")
                if path_ext == ".webp":
                    save_image_format = "WEBP"
                else:
                    save_image_format = mimetypes.guess_type(path)[0].split("/")[1]
                resize_width = int(config["image_compressor"]["width"])
                if is_images_dir and img.width > resize_width:
                    img = img.resize((resize_width,int(resize_width * img.height / img.width)))
                img_bytes = io.BytesIO()
                img.save(img_bytes, format=save_image_format)
                response_body = img_bytes.getvalue()
            except FileNotFoundError:
                if is_images_dir and path_ext == ".webp" and os.path.isfile(f"./images/{os.path.splitext(os.path.basename(path))[0]}"):
                    
                    img = Image.open(f"./images/{os.path.splitext(os.path.basename(path))[0]}",mode="r")
                    resize_width = int(config["image_compressor"]["width"])
                    if is_images_dir and img.width > resize_width:
                        img = img.resize((resize_width,int(resize_width * img.height / img.width)))
                    img_bytes = io.BytesIO()
                    img.save(img_bytes, format="WEBP")
                    response_body = img_bytes.getvalue()
                else:
                    request_status = 404
            
            self.send_response(request_status)
            self.send_header("Content-type", content_type)
            self.end_headers()
            self.wfile.write(response_body)

def main():
    if os.path.isfile("sl.json"):
        hostName = "localhost"
        serverPort = 8080
        webServer = HTTPServer((hostName, serverPort), SpiderServer)
        print("Server started http://%s:%s" % (hostName, serverPort))

        try:
            webServer.serve_forever()
        except KeyboardInterrupt:
            pass

        webServer.server_close()
        print("Server stopped.")
    else:
        sys.exit()
