import sys
import shutil
import os
import numpy as np
from PIL import Image
import torch
from setup import Net  # Import the CNN model from setup.py

# Instantiate the model and set it to evaluation mode
CNN_model = Net()
CNN_model.eval()

# Function to standardize the image
def standardize_image(image_path):
    image = Image.open(image_path).convert("RGB")
    img_array = np.array(image)
    mean = np.mean(img_array, axis=(0, 1))
    std = np.std(img_array, axis=(0, 1))
    standardized_img = (img_array - mean) / std
    standardized_img = np.clip(standardized_img, 0, 1)
    standardized_img = Image.fromarray((standardized_img * 255).astype(np.uint8))
    return standardized_img

# Function to classify the standardized image
def classify_image(image_path):
    image = Image.open(image_path).convert("RGB")
    image_tensor = transform_image_for_model(image)  # Transform for model input
    with torch.no_grad():
        output = CNN_model(image_tensor)
        _, predicted = torch.max(output, 1)
        label = "healthy" if predicted.item() == 0 else "unhealthy"
    return label

# Preprocessing: Convert the PIL image to a tensor for the model
def transform_image_for_model(image):
    # Assuming model expects 3x32x32 images, adjust if needed
    image = image.resize((32, 32))
    image = np.array(image).transpose((2, 0, 1))  # Rearrange dimensions to CxHxW
    image_tensor = torch.tensor(image, dtype=torch.float32).unsqueeze(0) / 255.0
    return image_tensor

# Upload and process the file
def upload_file(file_path, target_directory):
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    
    target_path = os.path.join(target_directory, os.path.basename(file_path))
    shutil.move(file_path, target_path)
    print(f"File '{file_path}' uploaded successfully to {target_path}")

    # Standardize and classify
    standardized_image = standardize_image(target_path)
    standardized_image.save(target_path)
    print(f"Image standardized and saved to {target_path}")

    # Classify image
    classification = classify_image(target_path)
    print(f"Image classified as: {classification}")

# Process all images in a folder
def upload_folder(folder_path, target_directory):
    if os.path.isdir(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                upload_file(file_path, target_directory)
    else:
        print(f"Folder '{folder_path}' does not exist.")

# Main
if __name__ == "__main__":
    target_directory = "/s/bach/l/under/carter64/public_html/uploads"
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
        upload_folder(folder_path, target_directory)
    else:
        print("No folder path provided.")
    if len(sys.argv == 1):
        folder_path = sys.argv[1]
        upload_folder(folder_path, target_directory)
    else:
        print("No Image Provided")
        

