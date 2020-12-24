def error(text):
    print(f"\033[31m\033[1mERROR\033[0m {text}")


def success(text):
    print(f"\033[32m\033[1mSUCCESS\033[0m {text}")


def warn(text):
    print(f"\033[33m\033[1mWARN\033[0m {text}")

def message(text):
    print(f"\033[34m\033[1mMESSAGE\033[0m {text}")