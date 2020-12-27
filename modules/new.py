import sys
import os
import modules.message
import modules.verification_values
import shutil
import subprocess
import json

def main():
    try:
        PROJECT_NAME = sys.argv[2]
    except IndexError:
        PROJECT_NAME = input("Input your project name:")
    if os.path.exists(PROJECT_NAME):
        modules.message.warn(
            f"Directory name is \"{PROJECT_NAME}\" with the same name directory exists.")
        overwrite_and_continue = input(
            "Do you want to overwrite and continue? (Y or anything else keys):")
        if modules.verification_values.yes_or_no(overwrite_and_continue):
            shutil.rmtree(PROJECT_NAME)
        else:
            modules.message.error(
                "Naming error (Intentional termination by you)")
            sys.exit()
    os.makedirs(PROJECT_NAME,exist_ok=True)
    os.chdir(PROJECT_NAME)
    stylesheet_type = input(
        "Which stylesheet types do you use, CSS or SCSS or SASS?:")
    while not stylesheet_type.upper() in ["CSS", "SCSS", "SASS"]:
        modules.message.error(f"Select Stylesheets type value is invalid.")
        stylesheet_type = input(
            "Which stylesheet types do you use, CSS or SCSS or SASS?:")
    using_git: str = input(
        "Would you like to use version control system (git):")
    if modules.verification_values.yes_or_no(using_git):
        try:
            subprocess.check_call("git --version", shell=True)
            subprocess.call("git init",shell=True)
            git_remote_url = input("Input your git remote repository url (If you do not have it,please input \"none\"):")
            if git_remote_url.lower() != "none":
                subprocess.call(f"git remote add origin {git_remote_url}", shell=True)
        except subprocess.CalledProcessError:
            modules.message.error("Git is not installed.")
            modules.message.message("Please check how to install git. https://git-scm.com/download")
    os.makedirs("assets/stylesheets", exist_ok=True)
    os.makedirs("assets/images", exist_ok=True)
    os.makedirs("assets/javascripts", exist_ok=True)
    os.makedirs("static", exist_ok=True)
    os.makedirs("pages", exist_ok=True)
    os.makedirs("layout", exist_ok=True)
    configuration = {
        "version": "0.0.1",
        "name": PROJECT_NAME,
        "stylesheets_file_format": stylesheet_type.lower(),
        "image_compressor": {
            "quality": 60,
            "width": 800,
        },
        "favicon_generater": {
            "path": "./static/favicon.png"
        }
    }
    with open("sl.json", "w",encoding="utf-8") as f:
        json.dump(configuration, f)
    modules.message.success("Finished making your new project.")