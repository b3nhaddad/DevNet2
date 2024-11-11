import sys
import shutil
import os
import numpy as np
from PIL import Image
import torch
from torch.utils.data import Dataset

def upload_file(file_path, target_directory):
    # Ensure the target directory exists
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    # Determine the target path
    target_path = os.path.join(target_directory, os.path.basename(file_path))

    # Move the file to the target directory
    shutil.move(file_path, target_path)
    print(f"File '{file_path}' uploaded successfully to {target_path}")

    # Standardize the image after uploading
    standardized_image = standardize_image(target_path)
    standardized_image.save(target_path)  # Overwrite with standardized version
    print(f"Image standardized and saved to {target_path}")

def upload_folder(folder_path, target_directory):
    # Ensure the folder exists
    if os.path.isdir(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):  # Check for file, not subfolder
                upload_file(file_path, target_directory)
    else:
        print(f"Folder '{folder_path}' does not exist.")

def standardize_image(image_path):
    # Open the image
    image = Image.open(image_path).convert("RGB")

    # Convert image to a numpy array
    img_array = np.array(image)

    # Calculate mean and standard deviation
    mean = np.mean(img_array, axis=(0, 1))
    std = np.std(img_array, axis=(0, 1))

    # Standardize the image
    standardized_img = (img_array - mean) / std

    # Clip values to [0, 1] range
    standardized_img = np.clip(standardized_img, 0, 1)

    # Convert back to PIL image
    standardized_img = Image.fromarray((standardized_img * 255).astype(np.uint8))

    return standardized_img

if __name__ == "__main__":
    # Define the target directory for uploads
    target_directory = "/s/bach/l/under/carter64/public_html/uploads"

    # Check if the folder path was provided
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
        upload_folder(folder_path, target_directory)
    else:
        print("No folder path provided.")


