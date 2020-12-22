import sys
import glob
import modules.message
import re
def build():
    files = glob.glob("./assets/stylesheets/**", recursive=True)
    re_scss_file_path = re.compile(r".*.scss")
    for file_name in files:
        if re_scss_file_path.fullmatch(file_name):
            print(file_name)

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