import torch
from torchvision import transforms
from PIL import Image
import numpy as np

def preprocess_image(path):
    img = Image.open(path).convert("L").resize((256,256))
    tensor = transforms.ToTensor()(img).unsqueeze(0)
    return tensor

def postprocess_image(tensor, save_path):
    arr = tensor.squeeze().detach().cpu().numpy()
    arr = (arr - arr.min()) / (arr.max() - arr.min() + 1e-8)
    img = Image.fromarray((arr*255).astype(np.uint8))
    img.save(save_path)

def run_cs_reconstruction(input_path, output_path, model, device):
    x_gt = preprocess_image(input_path).to(device)

    # Stage A: dummy CS (identity, can plug FISTA/NUFFT here)
    x0 = x_gt.clone()

    # Stage B: refinement
    with torch.no_grad():
        recon = model(x0)

    postprocess_image(recon, output_path)
