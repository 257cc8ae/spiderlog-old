import sys
from spiderlog.modules import new
from spiderlog.modules import message
from spiderlog.modules import build
from spiderlog.modules import version
from spiderlog.modules import server

def main():
    PROCESS_NAME: str = sys.argv[1]
    if PROCESS_NAME == "new":
        new.main()
    elif PROCESS_NAME == "build":
        build.main()
    elif PROCESS_NAME == "server" or PROCESS_NAME == "s":
        server.main()
    elif PROCESS_NAME == "--version" or "-v":
        print(version.returnVersion())
    else:
        message.error(f"Could not find PROCESS NAME \"{PROCESS_NAME}\"")
if __name__ == "__main__":
    main()