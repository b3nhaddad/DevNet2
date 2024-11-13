import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from PIL import Image
import os
import torch
from torch.utils.data import Dataset
import numpy as np
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
import shutil
from torchvision import transforms
from tqdm import tqdm
from torchvision import models


CNN_model = models.resnet18(weights=None)
num_features = CNN_model.fc.in_features
CNN_model.fc = nn.Linear(num_features, 2)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
CNN_model = CNN_model.to(device)

model_path = '/s/bach/l/under/carter64/public_html/cnn_model_weights.pth'
CNN_model.load_state_dict(torch.load(model_path, map_location=device))

CNN_model.eval()
