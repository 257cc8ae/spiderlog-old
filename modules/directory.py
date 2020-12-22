def new(path):
    directory_names = path.split("/")
    for directory_name in directory_names:
        if "." in directory_name:
            print("this is a file name")
        print(directory_name)