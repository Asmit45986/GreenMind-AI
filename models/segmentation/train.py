import os
import sys

# Safe environment settings
os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ["USE_CPU"] = "True"

import time
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import random_split, DataLoader

from models.segmentation.dataset import DeepGlobeDataset 
from models.segmentation.model import DeepLabModel

# =========================================================================
# CRITICAL: BUG BYPASS - ACCELERATOR HEALTH CHECK OVERRIDE
# =========================================================================
class PureCPUAdam(optim.Adam):
    """
    Standard Adam optimizer subclass that physically bypasses the buggy
    automatic accelerator graph capture health checks in PyTorch 2.x+ on CPU.
    """
    def _accelerator_graph_capture_health_check(self):
        # We dummy out this function completely so PyTorch never queries CUDA drivers!
        pass

# =========================================================================

def calculate_iou(preds, targets, num_classes=7):
    preds = torch.argmax(preds, dim=1)
    iou_list = []
    for cls in range(num_classes):
        pred_mask = (preds == cls)
        target_mask = (targets == cls)
        intersection = (pred_mask & target_mask).sum().item()
        union = (pred_mask | target_mask).sum().item()
        if union > 0:
            iou_list.append(intersection / union)
    return np.mean(iou_list) if len(iou_list) > 0 else 0.0

def run_training(epochs=5, batch_size=4, lr=1e-4):
    device = torch.device("cpu")
    print("❌ Hardware Acceleration Blocked. Running strictly on Pure CPU Mode...")

    # Safe dataset paths
    train_dir = r"D:\project data\AI_afforestation\datasets\DeepGlobeDataset\train"
    full_dataset = DeepGlobeDataset(image_dir=train_dir, mask_dir=train_dir, image_size=512)
    
    train_size = int(0.85 * len(full_dataset))
    val_size = len(full_dataset) - train_size
    train_dataset, val_dataset = random_split(full_dataset, [train_size, val_size])
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=0)

    # Force model load on CPU
    model = DeepLabModel(num_classes=7).to(device)
    criterion = nn.CrossEntropyLoss()
    
    # Using our customized optimizer that does not call accelerator hooks
    optimizer = PureCPUAdam(
        model.parameters(), 
        lr=lr, 
        weight_decay=1e-5, 
        foreach=False, 
        capturable=False
    )
    
    best_val_loss = float('inf')
    
    print(f"🚀 Starting Training Loop on CPU...")
    for epoch in range(epochs):
        start_time = time.time()
        model.train()
        train_loss, train_ious = 0.0, []
        for batch_idx, (images, masks) in enumerate(train_loader):
            images, masks = images.to(device), masks.to(device)
            
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, masks)
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
            train_ious.append(calculate_iou(outputs, masks))
            
            if (batch_idx + 1) % 10 == 0:
                print(f"Epoch [{epoch+1}/{epochs}] | Batch [{batch_idx+1}/{len(train_loader)}] | Loss: {loss.item():.4f}")
                
        model.eval()
        val_loss, val_ious = 0.0, []
        with torch.no_grad():
            for images, masks in val_loader:
                images, masks = images.to(device), masks.to(device)
                outputs = model(images)
                loss = criterion(outputs, masks)
                val_loss += loss.item()
                val_ious.append(calculate_iou(outputs, masks))
                
        epoch_val_loss = val_loss / len(val_loader)
        print(f"\n📢 Epoch {epoch+1} Done | Train Loss: {train_loss/len(train_loader):.4f} | Val Loss: {epoch_val_loss:.4f} | Val mIoU: {np.mean(val_ious):.4f}")
        
        if epoch_val_loss < best_val_loss:
            best_val_loss = epoch_val_loss
            # Safe cross-platform path check
            checkpoint_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "checkpoints")
            os.makedirs(checkpoint_dir, exist_ok=True)
            save_path = os.path.join(checkpoint_dir, "best_deeplab_model.pth")
            
            torch.save(model.state_dict(), save_path)
            print(f"💾 Saved best model weight checkpoint to: {save_path}")
            
        print(f"Epoch Time: {time.time() - start_time:.1f}s\n" + "-"*40)

if __name__ == "__main__":
    run_training(epochs=5)