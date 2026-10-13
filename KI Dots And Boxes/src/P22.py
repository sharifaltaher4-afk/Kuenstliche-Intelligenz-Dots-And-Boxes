import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

### Bilddaten werden in Tensoren umgewandelt (0–1 Werte statt Pixelwerte 0–255) Zahlenarray
transform = transforms.Compose([
    transforms.ToTensor(),

])

### Fashion-MNIST Trainingsdaten laden
train_dataset = datasets.FashionMNIST(
    root="data",
    train=True,
    download=True,
    transform=transform
)
### Testdaten laden
test_dataset = datasets.FashionMNIST(
    root="data",
    train=False,
    download=True,
    transform=transform
)

# Daten werden in kleine Batches aufgeteilt (64 Bilder pro Schritt)
# shuffle=True sorgt dafür, dass die Daten jedes Mal gemischt werden
batch_size = 64
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)


### Definition des neuronalen Netzes
class FashionNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.model = nn.Sequential(
            nn.Linear(28 * 28, 128),  # Eingabeschicht -> Hidden Layer
            nn.ReLU(),  # Aktivierungsfunktion
            nn.Dropout(0.2),  # Verhindert Overfitting
            nn.Linear(128, 10),  # Hidden Layer -> Ausgabeschicht
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.model(x)
        return logits
#NN1
class NN1(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.model = nn.Sequential(
            nn.Linear(28 * 28, 10)
        )

    def forward(self, x):
        x = self.flatten(x)
        return self.model(x)
#NN2
class NN2(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.model = nn.Sequential(
            nn.Linear(28 * 28, 128),
            nn.ReLU(),
            nn.Linear(128, 32),
            nn.ReLU(),
            #nn.Dropout(0.0),
            nn.Dropout(0.2),
            #nn.Dropout(0.5),
            nn.Linear(32, 10)
        )

    def forward(self, x):
        x = self.flatten(x)
        return self.model(x)

class NN2_ReLU(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.model = nn.Sequential(
            nn.Linear(28 * 28, 128),
            nn.ReLU(),
            nn.Linear(128, 32),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(32, 10)
        )

    def forward(self, x):
        x = self.flatten(x)
        return self.model(x)

class NN2_Sigmoid(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.model = nn.Sequential(
            nn.Linear(28 * 28, 128),
            nn.Sigmoid(),
            nn.Linear(128, 32),
            nn.Sigmoid(),
            nn.Dropout(0.2),
            nn.Linear(32, 10)
        )

    def forward(self, x):
        x = self.flatten(x)
        return self.model(x)

class NN2_Tanh(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.model = nn.Sequential(
            nn.Linear(28 * 28, 128),
            nn.Tanh(),
            nn.Linear(128, 32),
            nn.Tanh(),
            nn.Dropout(0.2),
            nn.Linear(32, 10)
        )

    def forward(self, x):
        x = self.flatten(x)
        return self.model(x)

#NN3
class NN3(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()

        self.model = nn.Sequential(
            nn.Linear(28 * 28, 64),
            nn.ReLU(),

            nn.Linear(64, 32),
            nn.ReLU(),

            nn.Linear(32, 16),
            nn.ReLU(),

            nn.Linear(16, 4),
            nn.ReLU(),

            nn.Linear(4, 4),
            nn.ReLU(),

            nn.Linear(4, 4),
            nn.ReLU(),

            nn.Linear(4, 8),
            nn.ReLU(),

            nn.Linear(8, 16),
            nn.ReLU(),

            nn.Linear(16, 10) # Ausgabeschicht. 10 Klassen
        )

    def forward(self, x):
        x = self.flatten(x)
        return self.model(x)

model = FashionNet()

### Test: ein Batch wird durch das Modell geschickt, ohne Training
examples, labels = next(iter(train_loader))
with torch.no_grad():
    predictions = model(examples)  #

### Umwandlung der Modell-Ausgabe in Wahrscheinlichkeiten (für Interpretation)
probabilities = torch.softmax(predictions, dim=1)

### Verlustfunktion: misst, wie weit die Vorhersagen von den echten Labels entfernt sind
loss_fn = nn.CrossEntropyLoss()
### passt die Gewichte des Netzes anhand des Fehlers an
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

### Testen des trainierten Modells auf den Testdaten
def test(dataloader, model, loss_fn):
    model.eval()
    test_loss = 0
    correct = 0
    total = 0

    with torch.no_grad():
        for X, y in dataloader:
            logits = model(X)
            loss = loss_fn(logits, y)
            test_loss += loss.item()
            preds = logits.argmax(dim=1)
            total += y.size(0)
            correct += (preds == y).sum().item()

    test_loss /= len(dataloader)
    accuracy = correct / total
    print(f"Test loss: {test_loss:.4f}, accuracy: {accuracy:.4f}")


### Trainingsfunktion (ein kompletter Durchlauf durch alle Daten)
def train(dataloader, model, loss_fn, optimizer):
    # Modell wird in Trainingsmodus gesetzt
    model.train()
    for batch, (X, y) in enumerate(dataloader):
        # ? Code fertig
        # 1. Vorwärtsdurchlauf: Modell macht Vorhersage
        pred = model(X)
        # 2. Fehler berechnen: Vergleich mit echten Labels
        loss = loss_fn(pred, y)

        # ? Code fertig
        # 3. Alte Gradienten löschen (wichtig für korrektes Lernen)
        optimizer.zero_grad()
        # 4. Rückwärtsdurchlauf: berechnet wie stark jedes Gewicht zum Fehler beiträgt
        loss.backward()
        # 5. Gewichte werden angepasst (Lernen passiert hier)
        optimizer.step()
        # Ausgabe des aktuellen Fehlers alle 100 Batches
        if batch % 100 == 0:
            print(
                f"loss: {loss.item():>7f}  "
                f"[{batch * len(X):>5d}/{len(dataloader.dataset):>5d}]"
            )

def compute_accuracy(dataloader, model):
    model.eval()  # kein Training

    correct = 0
    total = 0

    with torch.no_grad():
        for X, y in dataloader:
            outputs = model(X)

            # höchste Wahrscheinlichkeit = Vorhersage
            _, predicted = torch.max(outputs, 1)

            total += y.size(0)
            correct += (predicted == y).sum().item()

    return correct / total

def Aufgabe1():
    epochs = 5
    for t in range(epochs):
        print(f"Epoch {t + 1}\n-------------------------------")
        train(train_loader, model, loss_fn, optimizer)
    print("Training fertig!")
    print("\n" + "=" * 65)

#__________________________________________________________________________


def Aufgabe2():
    model = NN1()
    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    epochs = 5
    for t in range(epochs):
        print(f"NN1 - Epoch {t + 1}")
        train(train_loader, model, loss_fn, optimizer)
    acc_nn1 = compute_accuracy(train_loader, model)
    print("NN1 Accuracy:", acc_nn1)
    # __________________________________________Evaluation NN2_______________________
    print("\n" + "=" * 65)
    model = NN2()

    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    for t in range(epochs):
        print(f"NN2 - Epoch {t + 1}")
        train(train_loader, model, loss_fn, optimizer)
    acc_nn2 = compute_accuracy(train_loader, model)
    print("NN2 Accuracy:", acc_nn2)
    # _________________________Evaluation NN3__________________________________________
    print("\n" + "=" * 65)
    model = NN3()

    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    for t in range(epochs):
        print(f"NN3 - Epoch {t + 1}")
        train(train_loader, model, loss_fn, optimizer)
    acc_nn3 = compute_accuracy(train_loader, model)
    print("NN3 Accuracy:", acc_nn3)
    # __________________________________________________________________________
def Aufgabe4():
    epochs = 5
    model = NN2_ReLU()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    for t in range(epochs):
        print(f"NN2_ReLU - Epoch {t + 1}")
        train(train_loader, model, loss_fn, optimizer)

    acc_relu = compute_accuracy(train_loader, model)
    print("NN2_ReLU Accuracy:", acc_relu)
    # __________________________________________________________________________
    model = NN2_Sigmoid()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    for t in range(epochs):
        print(f"NN2_Sigmoid - Epoch {t + 1}")
        train(train_loader, model, loss_fn, optimizer)

    acc_sigmoid = compute_accuracy(train_loader, model)
    print("NN2_Sigmoid Accuracy:", acc_sigmoid)
    # __________________________________________________________________________
    model = NN2_Tanh()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    for t in range(epochs):
        print(f"NN2_Tanh - Epoch {t + 1}")
        train(train_loader, model, loss_fn, optimizer)

    acc_tanh = compute_accuracy(train_loader, model)
    print("NN2_Tanh Accuracy:", acc_tanh)
    # __________________________________________________________________________


def Aufgabe23():

    model = NN1()
    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    epochs = 5
    for t in range(epochs):
        print(f"NN1 - Epoch {t + 1}")
        train(train_loader, model, loss_fn, optimizer)
    test(test_loader, model, loss_fn)

    probability_model = nn.Sequential(
        model,
        nn.Softmax(dim=1)
    )

    examples, labels = next(iter(test_loader))
    print("True label:", labels[0].item())

    with torch.no_grad():
        probs = probability_model(examples[:1])

    print("Klassen-Wahrscheinlichkeiten:", probs[0])

    predicted_class = torch.argmax(probs[0]).item()
    print("Vorhergesagte Klasse:", predicted_class)

    # __________________________________________Evaluation NN2_______________________
    print("\n" + "=" * 65)
    model = NN2()
    epochs=5

    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    for t in range(epochs):
        print(f"NN2 - Epoch {t + 1}")
        train(train_loader, model, loss_fn, optimizer)
    test(test_loader, model, loss_fn)

    probability_model = nn.Sequential(
        model,
        nn.Softmax(dim=1)
    )

    examples, labels = next(iter(test_loader))
    print("True label:", labels[0].item())

    with torch.no_grad():
        probs = probability_model(examples[:1])

    print("Klassen-Wahrscheinlichkeiten:", probs[0])

    predicted_class = torch.argmax(probs[0]).item()
    print("Vorhergesagte Klasse:", predicted_class)
    # _________________________Evaluation NN3__________________________________________

    print("\n" + "=" * 65)
    model = NN3()

    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    for t in range(epochs):
        print(f"NN3 - Epoch {t + 1}")
        train(train_loader, model, loss_fn, optimizer)
    test(test_loader, model, loss_fn)

    probability_model = nn.Sequential(
        model,
        nn.Softmax(dim=1)
    )

    examples, labels = next(iter(test_loader))
    print("True label:", labels[0].item())

    with torch.no_grad():
        probs = probability_model(examples[:1])

    print("Klassen-Wahrscheinlichkeiten:", probs[0])

    predicted_class = torch.argmax(probs[0]).item()
    print("Vorhergesagte Klasse:", predicted_class)
    # __________________________________________________________________________


#Aufgabe1()
#Aufgabe2()
#Aufgabe4()
Aufgabe23()
 #_______________________________________Aufgabe 23_________________________________________________________



