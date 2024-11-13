import sys
import os
import requests
from PIL import Image
import torch
import numpy as np
from setup import Net

# Load the CNN model
CNN_model = Net()
CNN_model.eval()

def standardize_image(image_path):
    image = Image.open(image_path).convert("RGB")
    img_array = np.array(image)
    mean = np.mean(img_array, axis=(0, 1))
    std = np.std(img_array, axis=(0, 1))
    standardized_img = (img_array - mean) / std
    standardized_img = np.clip(standardized_img, 0, 1)
    standardized_img = Image.fromarray((standardized_img * 255).astype(np.uint8))
    return standardized_img

def classify_image(image_path):
    image = Image.open(image_path).convert("RGB")
    image_tensor = transform_image_for_model(image)
    with torch.no_grad():
        output = CNN_model(image_tensor)
        _, predicted = torch.max(output, 1)
        label = "healthy" if predicted.item() == 0 else "unhealthy"
    return label

def transform_image_for_model(image):
    image = image.resize((32, 32))  # Adjust as per model input size
    image = np.array(image).transpose((2, 0, 1))  # Convert to CxHxW
    image_tensor = torch.tensor(image, dtype=torch.float32).unsqueeze(0) / 255.0  # Add batch dimension
    return image_tensor

def send_classification_to_php(image_path, classification):
    # Send the classification result to a PHP script via POST
    php_url = "https://cs.colostate.edu/~bshaddad/uploadpy.php"  # URL of the PHP script
    data = {
        'image_path': image_path,
        'classification': classification  # Include classification result
    }
    response = requests.post(php_url, data=data)
    if response.status_code == 200:
        print("Successfully sent classification to PHP.")
    else:
        print("Failed to send classification to PHP.")

def main():
    if len(sys.argv) > 1:
        image_path = sys.argv[1]  # Get image path from command line argument
        print(f"Processing image: {image_path}")
        
        if os.path.exists(image_path):
            # Standardize and classify the image
            standardized_image = standardize_image(image_path)
            standardized_image.save(image_path)  # Save standardized image
            classification = classify_image(image_path)
            print(f"Image classified as: {classification}")
            
            # Send classification result to PHP
            send_classification_to_php(image_path, classification)
        else:
            print(f"Image file '{image_path}' does not exist.")
    else:
        print("No image path provided.")

if __name__ == "__main__":
    main()
