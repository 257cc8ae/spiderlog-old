from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import os
import sys
import json
import modules.spiderMark
import modules.message
import sass

def loadSLConfigFile():
    with open("sl.json", "r") as f:
        return json.load(f)

class SpiderServer(BaseHTTPRequestHandler):
    def do_GET(self):
        config = loadSLConfigFile()
        path = self.path
        if os.path.splitext(path)[-1] == ".css":
            try:
                with open(f"./assets/stylesheets/{os.path.splitext(os.path.basename(path))[0]}.{config['stylesheets_file_format']}", "r") as f:
                    self.send_response(200)
                    self.send_header("Content-type", "text/css")
                    self.end_headers()
                    self.wfile.write(bytes(sass.compile(string=f.read(), output_style='expanded'), "utf-8"))                    
            except FileNotFoundError:
                self.send_response(404)
                self.send_header("Content-type", "text/css")
                self.end_headers()
            except sass.CompileError:
                self.send_response(200)
                self.send_header("Content-type", "text/css")
                self.end_headers()
                self.wfile.write(bytes(f.read(), "utf-8"))   
        elif os.path.splitext(path)[-1] == ".js":
            try:
                with open(f"./javascripts/{os.path.basename(path)}", "r") as f:
                    self.send_response(200)
                    self.send_header("Content-type", "text/javascript")
                    self.end_headers()
                    self.wfile.write(bytes(f.read(), "utf-8"))   
            except FileNotFoundError:
                self.send_response(404)
                self.send_header("Content-type", "text/javascript")
                self.end_headers()

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