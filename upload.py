import sys
import shutil
import os
import numpy as np 
from PIL import Image 
import torch
from setup import Net 
# Import the CNN model from setup.py
# Instantiate the model and set it to evaluation mode
CNN_model = Net()
CNN_model.eval()


# Function to standardize the image
def standardize_image(image_path):
    image = Image.open(image_path).convert("RGB") #changes the color of the image
    img_array = np.array(image)
    mean = np.mean(img_array, axis=(0, 1))
    std = np.std(img_array, axis=(0, 1))
    standardized_img = (img_array - mean) / std
    standardized_img = np.clip(standardized_img, 0, 1) #smooths image over 0 to 1
    standardized_img = Image.fromarray((standardized_img * 255).astype(np.uint8))
    return standardized_img
#makes sure he image is standardized (in color, size, resolution )
# Function to classify the standardized image
def classify_image(image_path):
    image = Image.open(image_path).convert("RGB")
    image_tensor = transform_image_for_model(image)  # Transform for model input
    with torch.no_grad():
        output = CNN_model(image_tensor)  # Correct way to call the model
        _, predicted = torch.max(output, 1)
        label = "healthy" if predicted.item() == 0 else "unhealthy"
    return label

# Preprocessing: Convert the PIL image to a tensor for the model
def transform_image_for_model(image):
    image = image.resize((32, 32))  # Adjust size as required by the model
    image = np.array(image).transpose((2, 0, 1))  # Rearrange to CxHxW
    image_tensor = torch.tensor(image, dtype=torch.float32).unsqueeze(0) / 255.0  # Add batch dimension
    return image_tensor


# Function to handle file upload and processing
# Function to handle file upload and processing
def upload_file(file_path, target_directory):
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    
    target_path = os.path.join(target_directory, os.path.basename(file_path))
    
    # Check if source and destination are the same
    if os.path.abspath(file_path) == os.path.abspath(target_path):
        print(f"Source and target paths are the same: {file_path}")
    else:
        shutil.copy(file_path, target_path)  # Use copy instead of move if needed
    
    # Standardize and classify
    #the restandardization is needed to be properly classified
    standardized_image = standardize_image(target_path)
    standardized_image.save(target_path)
    print(f"Image standardized and saved to {target_path}")

    # Classify image
    classification = classify_image(target_path)
    #since this is a binary model classification is either healthy or unhealthy
    print(f"Image classified as: {classification}")

# Process all images in a folder
def upload_folder(folder_path, target_directory):
    if os.path.isdir(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                upload_file(file_path, target_directory)
    else:
        print(f"Folder '{folder_path}' does not exist.", file=sys.stderr)

# Main
if __name__ == "__main__":
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
        target_directory = "/s/parsons/g/under/bshaddad/public_html/uploads"
        upload_file(folder_path, target_directory)
    else:
        print("No folder path provided.", file=sys.stderr)



