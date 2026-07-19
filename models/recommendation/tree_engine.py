import numpy as np

class TreeRecommendationEngine:
    def __init__(self):
        # Master Tree Database: Har tree ki ideal growth conditions
        self.tree_database = {
            "Neem": {"land": ["barren", "rangeland"], "min_temp": 20, "max_temp": 45, "min_humidity": 15, "max_aqi": 5, "type": "Drought Resistant"},
            "Acacia (Babool)": {"land": ["barren"], "min_temp": 15, "max_temp": 48, "min_humidity": 10, "max_aqi": 5, "type": "Arid Hardy"},
            "Shisham": {"land": ["rangeland", "barren"], "min_temp": 10, "max_temp": 40, "min_humidity": 30, "max_aqi": 4, "type": "Timber Value"},
            "Bamboo": {"land": ["rangeland", "water_edge"], "min_temp": 15, "max_temp": 38, "min_humidity": 50, "max_aqi": 4, "type": "Soil Binder"},
            "Khejri": {"land": ["barren"], "min_temp": 10, "max_temp": 50, "min_humidity": 5, "max_aqi": 5, "type": "Desert Special"},
            "Amaltas": {"land": ["rangeland"], "min_temp": 15, "max_temp": 42, "min_humidity": 25, "max_aqi": 3, "type": "Eco-Balancer"}
        }

    def recommend_trees(self, land_type, env_profile):
        """
        land_type: 'barren' ya 'rangeland' (Model 1 se jo milega)
        env_profile: Fallback/Live JSON object jo API service se mila hai
        """
        # Dictionary parameters extract karna
        weather = env_profile.get('weather', {})
        air = env_profile.get('air_quality', {})
        
        current_temp = weather.get('temperature', 25.0)
        current_hum = weather.get('humidity', 50.0)
        aqi = air.get('aqi_index', 3)
        
        scored_recommendations = []
        
        for tree_name, specs in self.tree_database.items():
            # Condition 1: Land type match hona chahiye
            if land_type not in specs["land"]:
                continue
                
            # Condition 2: Temperature control limit
            if not (specs["min_temp"] <= current_temp <= specs["max_temp"]):
                continue
                
            # Initial Base Score
            score = 100
            
            # AQI stress management penalty
            if aqi > specs["max_aqi"]:
                score -= 30
                
            # Humidity adjustment
            if current_hum < specs["min_humidity"]:
                score -= 15
                
            scored_recommendations.append({
                "tree_name": tree_name,
                "type": specs["type"],
                "match_score": max(0, score)
            })
            
        # Descending order mein sort karna highest match rate ke sath
        return sorted(scored_recommendations, key=lambda x: x['match_score'], reverse=True)[:5]