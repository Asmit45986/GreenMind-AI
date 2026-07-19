import numpy as np

class TreeSurvivalPredictor:
    def __init__(self):
        # Har species ki sensitivity coefficients (Kitna temperature aur pollution jhel sakte hain)
        self.species_sensitivity = {
            "Neem": {"temp_optimal": 32, "aqi_tolerance": 5, "humidity_optimal": 35},
            "Acacia (Babool)": {"temp_optimal": 35, "aqi_tolerance": 5, "humidity_optimal": 20},
            "Shisham": {"temp_optimal": 28, "aqi_tolerance": 4, "humidity_optimal": 45},
            "Bamboo": {"temp_optimal": 26, "aqi_tolerance": 4, "humidity_optimal": 65},
            "Khejri": {"temp_optimal": 38, "aqi_tolerance": 5, "humidity_optimal": 15},
            "Amaltas": {"temp_optimal": 30, "aqi_tolerance": 3, "humidity_optimal": 40}
        }

    def predict_survival(self, tree_name, env_profile):
        """
        tree_name: Jis tree ki survival probability check karni hai
        env_profile: Weather aur AQI parameters ka data dictionary
        """
        weather = env_profile.get('weather', {})
        air = env_profile.get('air_quality', {})
        
        current_temp = weather.get('temperature', 25.0)
        current_hum = weather.get('humidity', 50.0)
        aqi = air.get('aqi_index', 3)
        
        # Base Survival Rate is 95% under perfect conditions
        survival_chance = 95.0
        confidence = 90.0 # Default confidence score
        
        specs = self.species_sensitivity.get(tree_name)
        if not specs:
            # Agar tree database mein nahi hai to baseline return karo
            return {"survival_percentage": 70.0, "confidence": 50.0, "risk_level": "Medium"}
            
        # 1. Temperature Deviation Penalty
        temp_diff = abs(current_temp - specs["temp_optimal"])
        if temp_diff > 5:
            survival_chance -= (temp_diff * 1.5) # Har extra degree par penalty
            
        # 2. AQI Stress Penalty
        if aqi >= specs["aqi_tolerance"]:
            survival_chance -= 15.0
            confidence -= 10.0 # Extreme settings down confidence
            
        # 3. Humidity Stress Penalty
        hum_diff = abs(current_hum - specs["humidity_optimal"])
        if hum_diff > 20:
            survival_chance -= (hum_diff * 0.3)

        # Bounds control (0% se 100% ke beech wrap karna)
        survival_chance = max(10.0, min(99.0, survival_chance))
        
        # Risk classification determine karna
        if survival_chance > 80:
            risk_level = "Low Risk (Highly Sustainable)"
        elif survival_chance > 50:
            risk_level = "Medium Risk (Requires Monitoring)"
        else:
            risk_level = "High Risk (Not Recommended)"
            
        return {
            "survival_percentage": round(survival_chance, 2),
            "confidence": round(confidence, 2),
            "risk_level": risk_level
        }