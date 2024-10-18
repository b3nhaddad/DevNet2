from PIL import Image
import os
import torch
from torch.utils.data import Dataset
import numpy as np

class PlantImageDataset(Dataset):
    def __init__(self, folder_path, transform=None):
        self.folder_path = folder_path
        self.image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
        self.transform = transform

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        img_name = self.image_files[idx]
        img_path = os.path.join(self.folder_path, img_name)
        image = Image.open(img_path)

        # Standardize image using the function
        image = self.standardize_image(image)

        # Apply any additional transformations if provided
        if self.transform:
            image = self.transform(image)

        return image, img_name  # Return image and its filename (optional)

    def standardize_image(self, image):
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

# Example usage:
if __name__ == '__main__':
    healthy_folder_path = '/Users/couchroomkid/Desktop/DevnetPlants/healthyImages'
    unhelathy_folder_path = '/Users/couchroomkid/Desktop/DevnetPlants/unhealthyImages'

    #above is the link to the files we want to use to actually create the neural network
    #I.E which images we will be adding
    #Below is the statements calling the dataset and how we instantiate these variables with type 'dataset'
    #dataset comes from torch (pytorch) and it is a way to simplfy smooted tensor data

    healthydataset = PlantImageDataset(healthy_folder_path)
    unhealthydataset = PlantImageDataset(unhelathy_folder_path)

    # To access data
    for i in range(len(healthydataset)):
        image, filename = healthydataset[i]
        print(f"Image {i}: {filename}, Size: {image.size}")


