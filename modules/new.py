import sys
def main():
    try:
        PROJECT_NAME = sys.argv[2]
    except IndexError:
        PROJECT_NAME = input("Input your project name:")
    print(PROJECT_NAME)