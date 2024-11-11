import sys
import shutil
import os

def upload_file(file_path):
    # Define the target directory
    target_directory = "/s/bach/l/under/carter64/public_html/uploads"

    # Ensure the target directory exists
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    # Determine the target path
    target_path = os.path.join(target_directory, os.path.basename(file_path))

    # Move the file to the target directory
    shutil.move(file_path, target_path)
    print(f"File uploaded successfully to {target_path}")

if __name__ == "__main__":
    # Check if the file path was provided
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        upload_file(file_path)
    else:
        print("No file path provided.")