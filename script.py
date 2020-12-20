import sys
import modules.message
def build():
    print("build function")

def main():
    PROCESS_NAME: str = sys.argv[1]
    if PROCESS_NAME == "build":
        build()
    else:
        modules.message.error(f"Could not find PROCESS NAME \"{PROCESS_NAME}\"")

if __name__ == "__main__":
    main()