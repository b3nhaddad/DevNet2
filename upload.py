import sys
import shutil
import os
from PIL import Image 
import torch
from torchvision import transforms  # Import transforms for image preprocessing
from setup import CNN_model  # Import the pre-trained ResNet model as CNN_model

# Classify the image
def classify_image(image_path):
    image = Image.open(image_path).convert("RGB")
    image_tensor = transform_image_for_model(image)  # Transform for model input
    CNN_model.eval()  # Make sure the model is in evaluation mode
    with torch.no_grad():
        output = CNN_model(image_tensor)  # Get the model output
        _, predicted = torch.max(output, 1)
        label = "Healthy" if predicted.item() == 0 else "Unhealthy"
    return label

# Transform the image for model input, resizing to 128x128
def transform_image_for_model(image):
    transform = transforms.Compose([
        transforms.Resize((128, 128)),  # Adjust to 128x128 as expected by the model
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])  # Use normalization values appropriate for the model
    ])
    image_tensor = transform(image).unsqueeze(0)  # Add batch dimension
    # Move tensor to the same device as CNN_model
    device = next(CNN_model.parameters()).device
    return image_tensor.to(device)

# Handle file upload and processing
def upload_file(file_path, target_directory):
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    
    target_path = os.path.join(target_directory, os.path.basename(file_path))
    
    # Check if source and destination are the same
    #if os.path.abspath(file_path) == os.path.abspath(target_path):
        #print(f"Source and target paths are the same: {file_path}")
    #else:
        #shutil.copy(file_path, target_path)  # Use copy instead of move if needed
    
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
        print(f"Folder '{folder_path}' does not exist.", file=sys.stderr)

# Main
if __name__ == "__main__":
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
        target_directory = "/s/bach/l/under/carter64/public_html/uploads"
        upload_file(folder_path, target_directory)
    else:
        print("No folder path provided.", file=sys.stderr)
