import os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, mean_absolute_error

def train_afforestation_ml_core():
    """
    Ye function hamare custom Master Dataset par Classifier aur Regressor 
    dono models ko train karke checkpoints save karega.
    """
    dataset_path = "datasets/master/master_dataset.csv"
    if not os.path.exists(dataset_path):
        print(f"❌ Master dataset missing at {dataset_path}!")
        return

    # 1. Load Dataset
    df = pd.read_csv(dataset_path)
    print("📋 Master Dataset Loaded. Shape:", df.shape)

    # 2. Encode Labels
    le_land = LabelEncoder()
    le_soil = LabelEncoder()
    le_tree = LabelEncoder()

    df['Land_Type_Enc'] = le_land.fit_transform(df['Land_Type'])
    df['Soil_Type_Enc'] = le_soil.fit_transform(df['Soil_Type'])
    df['Best_Tree_Enc'] = le_tree.fit_transform(df['Best_Tree'])

    # Features list matching Schema Design
    feature_cols = [
        'Vegetation_Percentage', 'Water_Nearby', 'Land_Type_Enc', 'Soil_Type_Enc', 
        'pH', 'Moisture', 'Temperature', 'Rainfall', 'Humidity', 'AQI', 'Elevation'
    ]
    
    X = df[feature_cols]
    y_tree = df['Best_Tree_Enc']
    y_survival = df['Survival_Probability']

    # Split
    X_train, X_test, y_tree_train, y_tree_test, y_surv_train, y_surv_test = train_test_split(
        X, y_tree, y_survival, test_size=0.2, random_state=42
    )

    # 3. Model 2 Training (Classifier)
    print("🤖 Training Model 2 (Tree Recommendation Classifier)...")
    clf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    clf_model.fit(X_train, y_tree_train)
    
    tree_preds = clf_model.predict(X_test)
    acc = accuracy_score(y_tree_test, tree_preds)
    print(f"✅ Model 2 Accuracy: {acc*100:.2f}%")

    # 4. Model 3 Training (Regressor)
    print("🤖 Training Model 3 (Survival Probability Regressor)...")
    reg_model = RandomForestRegressor(n_estimators=100, random_state=42)
    reg_model.fit(X_train, y_surv_train)
    
    surv_preds = reg_model.predict(X_test)
    mae = mean_absolute_error(y_surv_test, surv_preds)
    print(f"✅ Model 3 Mean Absolute Error: {mae:.2f}%")

    # 5. Save Artifacts
    os.makedirs("checkpoints", exist_ok=True)
    joblib.dump(clf_model, "checkpoints/tree_recommender.pkl")
    joblib.dump(reg_model, "checkpoints/survival_regressor.pkl")
    
    encoders = {'land': le_land, 'soil': le_soil, 'tree': le_tree, 'features': feature_cols}
    joblib.dump(encoders, "checkpoints/ml_encoders.pkl")
    
    print("💾 All ML Core Checkpoints saved successfully in 'checkpoints/'!")

if __name__ == "__main__":
    train_afforestation_ml_core()