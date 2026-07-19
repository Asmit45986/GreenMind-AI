import numpy as np

def calculate_all_metrics(pred_mask, gt_mask, num_classes=7):
    """
    Calculates Mean IoU, Dice/F1, Precision, and Recall across all classes.
    """
    iou_list = []
    dice_list = []
    precision_list = []
    recall_list = []
    
    for cls in range(num_classes):
        pred_cls = (pred_mask == cls)
        gt_cls = (gt_mask == cls)
        
        tp = np.logical_and(pred_cls, gt_cls).sum()
        fp = np.logical_and(pred_cls, np.logical_not(gt_cls)).sum()
        fn = np.logical_and(np.logical_not(pred_cls), gt_cls).sum()
        
        intersection = tp
        union = tp + fp + fn
        
        iou = intersection / union if union > 0 else 1.0
        iou_list.append(iou)
        
        precision = tp / (tp + fp) if (tp + fp) > 0 else 1.0
        precision_list.append(precision)
        
        recall = tp / (tp + fn) if (tp + fn) > 0 else 1.0
        recall_list.append(recall)
        
        dice = (2 * tp) / (2 * tp + fp + fn) if (2 * tp + fp + fn) > 0 else 1.0
        dice_list.append(dice)
        
    return {
        "mIoU": np.mean(iou_list),
        "Dice_F1": np.mean(dice_list),
        "Precision": np.mean(precision_list),
        "Recall": np.mean(recall_list)
    }