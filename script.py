import sys
import glob
import re
import sass
import os
import modules.directory
import modules.message

def build():
    # os.makedirs(os.path.join("dist","stylesheets"), exist_ok=True)
    files = glob.glob("./assets/stylesheets/**", recursive=True)
    re_scss_file_path = re.compile(r".\/assets\/stylesheets\/(.*).scss")
    for file_name in files:
        if re_scss_file_path.fullmatch(file_name):
            print(os.path.join("dist","stylesheets",f"{re_scss_file_path.match(file_name).group(1)}.css"))
            with open(file_name, "r") as f:
                try:
                    css_code = sass.compile(string = f.read(), output_style='compressed')
                    print(css_code)
                    modules.directory.new(os.path.join("dist","stylesheets",f"{re_scss_file_path.match(file_name).group(1)}.css"))
                    # with open(os.path.join("dist","stylesheets",f"{re_scss_file_path.match(file_name).group(1)}.css"),"w") as css_file:
                    #     f.write(css_code)
                except sass.CompileError:
                    pass

                
                
            
def main():
    try:
        PROCESS_NAME: str = sys.argv[1]
        if PROCESS_NAME == "build":
            build()
        else:
            modules.message.error(f"Could not find PROCESS NAME \"{PROCESS_NAME}\"")
    except IndexError:
        modules.message.error("No argument is specified.")

if __name__ == "__main__":
    main()