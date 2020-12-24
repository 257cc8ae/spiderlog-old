import os
import modules.message
import json
def main():
    try:
        with open("sl.json","w") as f:
            configuration = json.load(f)
            print(configuration)
    except FileNotFoundError:
        modules.message.error("This is not the SpiderLog directory.")