import subprocess

def read_file_content(file_path):
    file_content = ""
    
    with open(file_path, 'r') as file:
        file_content = file.read()

    return file_content

def run_shell_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip()