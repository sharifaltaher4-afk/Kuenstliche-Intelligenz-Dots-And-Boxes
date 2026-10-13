import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

print("PyTorch:", torch.__version__)

# Fashion-MNIST laden
dataset = datasets.FashionMNIST(
    root="data",
    train=True,
    download=True,
    transform=transforms.ToTensor()
)

print("Anzahl Bilder:", len(dataset))

bild, label = dataset[0]

print("Bildform:", bild.shape)
print("Label:", label)

loader = DataLoader(dataset, batch_size=64)

bilder, labels = next(iter(loader))

print("Batch-Form:", bilder.shape)
print("Labels-Form:", labels.shape)