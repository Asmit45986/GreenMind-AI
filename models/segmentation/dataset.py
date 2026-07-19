import os
import cv2
import torch
import numpy as np
from torch.utils.data import Dataset

COLOR_MAP = {
    (0, 255, 255): 0,    # urban_land (Cyan)
    (255, 255, 0): 1,    # agriculture_land (Yellow)
    (255, 0, 255): 2,    # rangeland (Magenta)
    (0, 255, 0): 3,      # forest_land (Green)
    (0, 0, 255): 4,      # water (Blue)
    (255, 255, 255): 5,  # barren_land (White)
    (0, 0, 0): 6         # unknown (Black)
}

def rgb_to_label(mask_rgb):
    """
    Super-fast vectorized RGB to label mapping (No memory leaks).
    """
    h, w, _ = mask_rgb.shape
    label_mask = np.zeros((h, w), dtype=np.int64)
    for rgb, class_id in COLOR_MAP.items():
        match = (mask_rgb[:, :, 0] == rgb[0]) & \
                (mask_rgb[:, :, 1] == rgb[1]) & \
                (mask_rgb[:, :, 2] == rgb[2])
        label_mask[match] = class_id
    return label_mask

class DeepGlobeDataset(Dataset):
    def __init__(self, image_dir, mask_dir, image_size=512):
        self.image_dir = image_dir
        self.mask_dir = mask_dir
        self.image_size = image_size
        
        # Sahi matching images aur masks find karna
        all_files = os.listdir(image_dir)
        self.image_paths = sorted([os.path.join(image_dir, f) for f in all_files if f.endswith('_sat.jpg')])
        self.mask_paths = sorted([os.path.join(mask_dir, f) for f in all_files if f.endswith('_mask.png')])
        
        if len(self.image_paths) == 0:
            raise RuntimeError(f"No matching images found in {image_dir}!")

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, index):
        image = cv2.imread(self.image_paths[index])
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        mask = cv2.imread(self.mask_paths[index])
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2RGB)
        
        image = cv2.resize(image, (self.image_size, self.image_size))
        mask = cv2.resize(mask, (self.image_size, self.image_size), interpolation=cv2.INTER_NEAREST)
        
        mask_labeled = rgb_to_label(mask)
        
        image_tensor = torch.from_numpy(image).permute(2, 0, 1).float() / 255.0
        mask_tensor = torch.from_numpy(mask_labeled).long()
        
        return image_tensor, mask_tensor