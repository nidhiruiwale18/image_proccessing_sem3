import torch
import torch.nn as nn

class UNet(nn.Module):
    def _init_(self, in_ch=1, out_ch=1, base=32):
        super()._init_()
        self.enc1 = nn.Sequential(
            nn.Conv2d(in_ch, base, 3, padding=1), nn.ReLU(),
            nn.Conv2d(base, base, 3, padding=1), nn.ReLU()
        )
        self.pool = nn.MaxPool2d(2)
        self.final = nn.Conv2d(base, out_ch, 1)

    def forward(self, x):
        e1 = self.enc1(x)
        p1 = self.pool(e1)
        out = self.final(e1)   # minimal version
        return out

class ReconModel(nn.Module):
    def _init_(self):
        super()._init_()
        self.refiner = UNet()

    def forward(self, x):
        return self.refiner(x)
