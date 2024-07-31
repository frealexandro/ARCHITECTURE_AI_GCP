import os
import subprocess
import sys

def execute_bash(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing bash command: {e}")
        sys.exit(1)

def execute_python(code):
    try:
        exec(code)
    except Exception as e:
        print(f"Error executing Python code: {e}")
        sys.exit(1)

def process_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read().strip()
        lines = content.split('\n')
        
        if lines[0] == '[bash]':
            execute_bash('\n'.join(lines[1:]))
        elif lines[0] == '[python]':
            execute_python('\n'.join(lines[1:]))
        elif lines[0] == '[txt]':
            # For [txt] files, we'll just print the content
            print("Text content:")
        else:
            print(f"Unknown file type in {file_path}")

def main():
    # List all .txt files in the current directory
    txt_files = sorted([f for f in os.listdir('.') if f.endswith('.txt')])
    
    for file in txt_files:
        print(f"Processing file: {file}")
        process_file(file)
        print(f"Finished processing: {file}\n")

if __name__ == "__main__":
    main()