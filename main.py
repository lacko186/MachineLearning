import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, Subset
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix
import seaborn as sns


class Háló(nn.Module):
    def __init__(self, szam=10):
        super(Háló, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, szam)
        self.medence = nn.MaxPool2d(kernel_size=2, stride=2, padding=0)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.25)

    def forward(self, x):
        x = self.medence(self.relu(self.conv1(x)))
        x = self.medence(self.relu(self.conv2(x)))
        x = x.view(-1, 64 * 7 * 7)
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return x


def betanitas(modell, adatok, veszteseg_fn, optimalizalo, feldolgozasszama=5):
    modell.train()
    for epoka in range(feldolgozasszama):
        osszes_veszteseg = 0.0
        for kepek, cimkek in adatok:
            optimalizalo.zero_grad()
            kimenetek = modell(kepek)
            veszteseg = veszteseg_fn(kimenetek, cimkek)
            veszteseg.backward()
            optimalizalo.step()
            osszes_veszteseg += veszteseg.item()
        print(f'[{epoka+1}/{feldolgozasszama}] Veszteség: {osszes_veszteseg/len(adatok):.4f}')
    print('Tanítás befejezve!')
    return modell


def ertekeles(modell, teszt_adatok):
    modell.eval()
    osszes_joslat = []

    with torch.no_grad():
        for kepek, _ in teszt_adatok:
            kimenetek = modell(kepek)
            _, joslat = torch.max(kimenetek.data, 1)
            osszes_joslat.extend(joslat.cpu().numpy())
    return osszes_joslat


def abrazolas(igazi_cimkek, joslott_cimkek, osztalyok):
    cm = confusion_matrix(igazi_cimkek, joslott_cimkek)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=osztalyok, yticklabels=osztalyok)
    plt.ylabel('Valódi')
    plt.xlabel('Jósolt')
    plt.title('Összetévesztési Mátrix')
    plt.show()


def pontossag_szamitas(igazi_cimkek, joslott_cimkek):
    helyes = sum(i == j for i, j in zip(igazi_cimkek, joslott_cimkek))
    pont = helyes / len(igazi_cimkek) * 100
    return pont


def main():
    koteg_meret = 64
    tanulasi_rata = 0.001
    feldolgozasszama = 5
    
    tanito_kepek_szama = 100
    teszt_kepek_szama = 10

    transzformacio = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))
    ])

    teljes_tanito_adathalmaz = datasets.MNIST(root='./data', train=True, transform=transzformacio, download=True)
    teljes_teszt_adathalmaz = datasets.MNIST(root='./data', train=False, transform=transzformacio, download=True)

    tanito_indexek = list(range(tanito_kepek_szama))
    teszt_indexek = list(range(teszt_kepek_szama))
    
    tanito_adathalmaz = Subset(teljes_tanito_adathalmaz, tanito_indexek)
    teszt_adathalmaz = Subset(teljes_teszt_adathalmaz, teszt_indexek)

    adatok = DataLoader(dataset=tanito_adathalmaz, batch_size=koteg_meret, shuffle=True)
    teszt_adatok = DataLoader(dataset=teszt_adathalmaz, batch_size=koteg_meret, shuffle=False)

    print(f'train kép száma: {len(tanito_adathalmaz)}')
    print(f'teszt kép száma: {len(teszt_adathalmaz)}')

    modell = Háló(szam=10)
    veszteseg_fuggveny = nn.CrossEntropyLoss()
    optimalizalo = optim.Adam(modell.parameters(), lr=tanulasi_rata)

    modell = betanitas(modell, adatok, veszteseg_fuggveny, optimalizalo, feldolgozasszama)

    igazi_cimkek = []
    for _, cimkek in teszt_adatok:
        igazi_cimkek.extend(cimkek.numpy())
    
    joslott_cimkek = ertekeles(modell, teszt_adatok)

    pont = pontossag_szamitas(igazi_cimkek, joslott_cimkek)
    print(f'\nModell pontossága: {pont:.2f}%')

    osztalyok = [str(i) for i in range(10)]
    abrazolas(igazi_cimkek, joslott_cimkek, osztalyok)


if __name__ == '__main__':
    main()