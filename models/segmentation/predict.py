import os
import torch
import numpy as np
import matplotlib.pyplot as plt
from models.segmentation.model import DeepLabModel
from models.segmentation.metrics import calculate_all_metrics

COLOR_MAP = {
    0: (0, 255, 255),    # urban_land (Cyan)
    1: (255, 255, 0),    # agriculture_land (Yellow)
    2: (255, 0, 255),    # rangeland (Magenta)
    3: (0, 255, 0),      # forest_land (Green)
    4: (0, 0, 255),      # water (Blue)
    5: (255, 255, 255),  # barren_land (White)
    6: (0, 0, 0)         # unknown (Black)
}

def label_to_rgb(mask_labeled):
    h, w = mask_labeled.shape
    rgb_mask = np.zeros((h, w, 3), dtype=np.uint8)
    for class_id, rgb in COLOR_MAP.items():
        rgb_mask[mask_labeled == class_id] = rgb
    return rgb_mask

def load_saved_model(weight_path="best_deeplab_model.pth", num_classes=7):
    device = torch.device("cpu")
    model = DeepLabModel(num_classes=num_classes)
    
    if not os.path.exists(weight_path):
        raise FileNotFoundError(f"Weight file not found at: {weight_path}")
        
    model.load_state_dict(torch.load(weight_path, map_location=device))
    model.to(device)
    model.eval()
    print(f"✅ Loaded model from {weight_path}")
    return model, device

def run_evaluation_visual(image_tensor, mask_tensor, model, device):
    """
    Predicts, calculates evaluation metrics on Ground Truth, and plots side-by-side.
    """
    img_batch = image_tensor.unsqueeze(0).to(device)
    
    with torch.no_grad():
        output = model(img_batch)
        prediction = torch.argmax(output, dim=1).squeeze(0).cpu().numpy()
        
    original_img = image_tensor.permute(1, 2, 0).cpu().numpy()
    ground_truth = mask_tensor.cpu().numpy()
    
    # Calculate performance metrics
    metrics = calculate_all_metrics(prediction, ground_truth)
    
    # Print metrics on console
    print("\n" + "="*30 + " EVALUATION METRICS " + "="*30)
    print(f"📈 Mean IoU (mIoU):     {metrics['mIoU']:.4f}  ({metrics['mIoU']*100:.1f}%)")
    print(f"🧬 Dice Score (F1):    {metrics['Dice_F1']:.4f}  ({metrics['Dice_F1']*100:.1f}%)")
    print(f"🎯 Precision:           {metrics['Precision']:.4f}  ({metrics['Precision']*100:.1f}%)")
    print(f"🔍 Recall:              {metrics['Recall']:.4f}  ({metrics['Recall']*100:.1f}%)")
    print("="*80 + "\n")
    
    # Convert back to RGB for visualization
    gt_rgb = label_to_rgb(ground_truth)
    pred_rgb = label_to_rgb(prediction)
    
    # Plotting
    plt.figure(figsize=(15, 5))
    
    plt.subplot(1, 3, 1)
    plt.imshow(original_img)
    plt.title("Satellite Image", fontsize=12)
    plt.axis("off")
    
    plt.subplot(1, 3, 2)
    plt.imshow(gt_rgb)
    plt.title("Ground Truth Mask", fontsize=12)
    plt.axis("off")
    
    plt.subplot(1, 3, 3)
    plt.imshow(pred_rgb)
    plt.title(f"Predicted Mask\n(mIoU: {metrics['mIoU']*100:.1f}%)", fontsize=12)
    plt.axis("off")
    
    plt.tight_layout()
    plt.show()
    
    return metrics