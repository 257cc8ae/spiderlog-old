import sys
import modules.new
import modules.message
import modules.build
import modules.version

def main():
    PROCESS_NAME: str = sys.argv[1]
    if PROCESS_NAME == "new":
        modules.new.main()
    elif PROCESS_NAME == "build":
        modules.build.main()
    elif PROCESS_NAME == "--version" or "-v":
        print(modules.version.returnVersion())
    else:
        modules.message.error(f"Could not find PROCESS NAME \"{PROCESS_NAME}\"")
if __name__ == "__main__":
    main()