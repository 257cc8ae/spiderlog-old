import sys
import glob
import re
import sass
import os
import time
import modules.new
import modules.message
import modules.build

def main():
    PROCESS_NAME: str = sys.argv[1]
    if PROCESS_NAME == "new":
        modules.new.main()
    elif PROCESS_NAME == "build":
        modules.build.main()
    else:
        modules.message.error(f"Could not find PROCESS NAME \"{PROCESS_NAME}\"")


if __name__ == "__main__":
    main()