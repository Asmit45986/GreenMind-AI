class CarbonCreditEstimator:
    def __init__(self):
        # Average annual CO2 absorption rate per tree (in kg/year) jab tree mature ho jaye
        # reference standard data for diverse species
        self.carbon_absorption_rates = {
            "Neem": 22.0,
            "Acacia (Babool)": 18.5,
            "Shisham": 25.0,
            "Bamboo": 12.0,  # Single culm, but grows fast in clusters
            "Khejri": 15.0,
            "Amaltas": 19.0
        }

    def estimate_carbon_credits(self, tree_name, tree_count, survival_percentage, project_years=10):
        """
        tree_name: Tree species ka naam
        tree_count: Total kitne trees plant karne ka plan hai
        survival_percentage: Phase 9 se aaya hua survival rate (%)
        project_years: Kitne saalon ke liye baseline projection chahiye (Default: 10 Years)
        """
        annual_rate_per_tree = self.carbon_absorption_rates.get(tree_name, 20.0) # Fallback 20kg
        
        # Effective number of trees based on survival probability
        effective_trees = tree_count * (survival_percentage / 100.0)
        
        # Total annual CO2 absorption in kg
        annual_co2_kg = effective_trees * annual_rate_per_tree
        
        # Total CO2 absorption over project duration in Metric Tons
        total_co2_tons = (annual_co2_kg * project_years) / 1000.0
        
        # Standard Global Rule: 1 Carbon Credit = 1 Metric Ton of CO2 stored
        carbon_credits_earned = total_co2_tons
        
        # Estimated financial value (Standard market average assumption: $15 - $25 per credit)
        estimated_revenue_usd = carbon_credits_earned * 20.0 
        
        return {
            "effective_active_trees": round(effective_trees),
            "annual_co2_absorbed_kg": round(annual_co2_kg, 2),
            "total_co2_absorbed_tons": round(total_co2_tons, 2),
            "carbon_credits": round(carbon_credits_earned, 2),
            "estimated_revenue_inr": round(estimated_revenue_usd * 83.5, 2) # Converting to INR
        }