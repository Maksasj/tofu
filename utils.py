def read_file_content(file_path):
    file_content = ""
    
    with open(file_path, 'r') as file:
        file_content = file.read()

    return file_content