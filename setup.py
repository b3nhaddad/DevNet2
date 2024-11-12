import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3,6,5)
        self.pool1 = nn.MaxPool2d(2,2)
        self.conv2 = nn.Conv2d(6,16, 5)
        self.fc1 = nn.Linear(20, 520)
        self.fc2 = nn.Linear(520, 2)


    def forward(self):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = torch.flatten(x, 1)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

CNN_model = Net()
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(CNN_model.parameters())
