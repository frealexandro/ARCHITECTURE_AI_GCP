import os
import subprocess
import sys
import re


def execute_bash(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing bash command: {e}")
        sys.exit(1)

def create_python_file(code, file_name):
    try:
        with open(file_name, 'w') as py_file:
            py_file.write(code)
        print(f"Created Python file: {file_name}")
    except Exception as e:
        print(f"Error creating Python file: {e}")
        sys.exit(1)

def handle_requirements(content, file_name):
    try:
        with open(file_name, 'w') as req_file:
            req_file.write(content)
        print(f"Created requirements file: {file_name}")
    except Exception as e:
        print(f"Error creating requirements file: {e}")
        sys.exit(1)


def process_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Split content into sections based on headers, including the content before the first header
    sections = re.split(r'(\[(?:bash|python|txt)\])', content)
    
    current_type = None
    current_content = ""

    for section in sections:
        if section.strip() in ['[bash]', '[python]', '[txt]']:
            if current_type:
                process_section(current_type, current_content.strip(), file_path)
            current_type = section.strip()[1:-1]  # Remove brackets
            current_content = ""
        else:
            current_content += section

    # Process the last section
    if current_type:
        process_section(current_type, current_content.strip(), file_path)


def process_section(content_type, content, file_path):
    if content_type == 'bash':
        print(f"Executing bash commands from {file_path}")
        execute_bash(content)
    elif content_type == 'python':
        python_file_name = f"{os.path.splitext(file_path)[0]}.py"
        create_python_file(content, python_file_name)
    elif content_type == 'txt':
        if 'requirements.txt' in file_path.lower():
            handle_requirements(content, 'requirements.txt')
        else:
            print(f"Text content from {file_path}:")
            print(content)
    else:
        print(f"Unknown content type '{content_type}' in {file_path}")


def run():

    #! the process starts here
    directory = '/home/frealexandro/proyectos_personales/gemini_pro_competition/api/final_output'

    # List all code_blocks_1.txt, code_blocks_2.txt files in the specified directory
    txt_files = [file for file in os.listdir(directory) if file.startswith("code_blocks_") and file.endswith(".txt")]

    # Sort files based on the number in their name
    txt_files.sort(key=lambda f: int(re.search(r'code_blocks_(\d+)', f).group(1)))
    
    for file in txt_files:
        file_path = os.path.join(directory, file)
        print(f"Processing file: {file}")
        process_file(file_path)
        print(f"Finished processing: {file}\n")


if __name__ == "__main__":
    run()