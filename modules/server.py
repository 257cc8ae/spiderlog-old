from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import os
import sys
import json
import re
import modules.spiderMark
import modules.message
import sass
import mimetypes

def loadSpiderLogConfigFile():
    try:
        with open("sl.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        modules.message.error("This is not the SpiderLog directory.")
        sys.exit()

def isBinaryOrText(mimetype):
    mimetype_type = mimetype.split("/")[0]
    if  mimetype_type == "text" or mimetype_type == "application" or mimetype == "image/svg+xml":
        return True
    else:
        return False

class SpiderServer(BaseHTTPRequestHandler):
    def do_GET(self):
        config = loadSpiderLogConfigFile()
        path = self.path
        path_ext = os.path.splitext(path)[-1]
        content_type = mimetypes.guess_type(path)[0]
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
            self.send_response(request_status)
            self.send_header("Content-type", content_type)
            self.end_headers()
            self.wfile.write(bytes(response_body, "utf-8"))
        else:
            print("fuck")
            self.send_response(request_status)
            self.send_header("Content-type", content_type)
            self.end_headers()
            with open("./static/favicon.png","rb") as f:
                response_body = f.read()
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
