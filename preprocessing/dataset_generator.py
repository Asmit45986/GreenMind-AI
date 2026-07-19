import os
import pandas as pd
import numpy as np

def generate_master_dataset(num_samples=1200):
    np.random.seed(42)
    data = {
        "Image_ID": [f"img{str(i).zfill(3)}" for i in range(1, num_samples + 1)],
        "Land_Type": np.random.choice(["Barren", "Rangeland", "Forest", "Agriculture", "Urban"], num_samples),
        "Vegetation_Percentage": np.random.uniform(5.0, 85.0, num_samples),
        "Water_Nearby": np.random.choice([1, 0], num_samples, p=[0.3, 0.7]),
        "Soil_Type": np.random.choice(["Sandy", "Loamy", "Clayey", "Rocky", "Alluvial"], num_samples),
        "pH": np.random.uniform(5.5, 8.5, num_samples),
        "Moisture": np.random.uniform(10.0, 80.0, num_samples),
        "Temperature": np.random.uniform(15.0, 45.0, num_samples),
        "Rainfall": np.random.uniform(200.0, 1200.0, num_samples),
        "Humidity": np.random.uniform(20.0, 90.0, num_samples),
        "AQI": np.random.randint(30, 400, num_samples),
        "Elevation": np.random.uniform(50.0, 2000.0, num_samples),
    }
    df = pd.DataFrame(data)
    
    def assign_target(row):
        if row['Land_Type'] == "Barren" and row['Rainfall'] < 500:
            return "Neem" if row['Soil_Type'] in ["Sandy", "Alluvial"] else "Acacia"
        elif row['Land_Type'] == "Rangeland" and row['Temperature'] < 30:
            return "Shisham" if row['Soil_Type'] == "Loamy" else "Bamboo"
        elif row['Water_Nearby'] == 1 and row['Humidity'] > 60:
            return "Jamun"
        else:
            return "Amaltas"
            
    df['Best_Tree'] = df.apply(assign_target, axis=1)
    
    def calculate_survival(row):
        base_survival = 95.0
        if row['AQI'] > 250: base_survival -= 15
        if row['Temperature'] > 40: base_survival -= 10
        if row['Rainfall'] < 300: base_survival -= 12
        return max(40.0, min(98.0, base_survival + np.random.uniform(-5, 3)))
        
    df['Survival_Probability'] = df.apply(calculate_survival, axis=1).round(2)
    
    # 💡 Yeh line ensure karegi ki datasets/master folder automatic ban jaye
    os.makedirs("datasets/master", exist_ok=True)
    output_path = "datasets/master/master_dataset.csv"
    df.to_csv(output_path, index=False)
    print(f"✅ CSV Generated at: {output_path} | Shape: {df.shape}")

if __name__ == "__main__":
    generate_master_dataset()