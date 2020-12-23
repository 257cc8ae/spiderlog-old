import sys
import os
import modules.message
def main():
    try:
        PROJECT_NAME = sys.argv[2]
    except IndexError:
        PROJECT_NAME = input("Input your project name:")
    if os.path.exists(PROJECT_NAME):
        modules.message.warn(f"Directory name is \"{PROJECT_NAME}\" with the same name directory exists.")
        overwrite_and_continue = input("Do you want to overwrite and continue? (Y or anything else keys):")
    if overwrite_and_continue != "Y" or overwrite_and_continue != "y":
        modules.message.error("Naming error (Intentional termination by you)")     