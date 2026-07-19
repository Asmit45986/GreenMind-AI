Markdown
# 🌲 GreenMind AI – Full-Stack Afforestation & Carbon Analytics SaaS Platform

[![React](https://img.shields.io/badge/Frontend-React.js-blue?style=for-the-badge&logo=react)](https://react.dev/)
[![Node.js](https://img.shields.io/badge/Backend-Node.js%20%7C%20Express-green?style=for-the-badge&logo=nodedotjs)](https://nodejs.org/)
[![Python](https://img.shields.io/badge/ML%20Engine-Python%203-yellow?style=for-the-badge&logo=python)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/ML%20Library-Scikit--Learn-orange?style=for-the-badge&logo=scikitlearn)](https://scikit-learn.org/)
[![Deployment](https://img.shields.io/badge/Hosted-Render%20Cloud-black?style=for-the-badge&logo=render)](https://render.com/)

An advanced full-stack AI platform designed to optimize ecological afforestation strategies. The platform integrates pre-trained Machine Learning models with a production-grade Web architecture to evaluate terrain telemetry and deliver deep environmental and financial analytics.

---

## 🚀 Live Demo & Video Walkthrough
* **Live Web Application:** [Insert Render Frontend Link Here]
* **Project Video Demonstration:** *(Video Walkthrough Link Coming Soon)*

---

## 🏛️ System Architecture & Data Flow

The platform relies on a decoupled microservices-like architecture, connecting an asynchronous Node.js runtime with an isolated Python ML computational environment.

[ React.js Frontend ]
│
▼ (HTTPS POST / JSON Telemetry)
[ Node.js + Express API Gateway ]
│
├─► (Dynamic Environment Detection: Local Windows venv vs Render Linux native)
├─► (Generates Temporary Secure Input Context)
│
▼ (Asynchronous Execution via child_process execFile)
[ Python Bridge Controller Engine ]
│
├─► (Loads Joblib-Serialized Scikit-Learn Model Checkpoints)
├─► (Evaluates 11 Environmental Target Features)
├─► (Computes Dynamic Classifier Probability Matrices)
│
▼ (Standard Output Broadcast)
[ Node.js API Gateway ] ➔ [ React UI Interactive Dashboard ]


---

## ✨ Core Functional Features

* **Dynamic Terrain Analytics:** Evaluates 11 key environmental metrics (including Soil pH, Vegetation %, Water Proximity, Rainfall, AQI, Elevation, and Temperature) to evaluate ecological feasibility.
* **Hybrid ML Pipeline:** Utilizes specialized predictive checkpoint pipelines:
  * **Tree Classifier (`tree_recommender.pkl`):** Classifies optimal botanical recommendations based on terrain compatibility.
  * **Survival Regressor (`survival_regressor.pkl`):** Predicts long-term tree survivability coefficients under specified environmental stresses.
* **Dynamic Confidence Evaluation:** Implements dynamic evaluation frameworks (`predict_proba`) to compute exact mathematical certainty scores for real-time predictions.
* **Carbon Accounting Engine:** Automatically models a 10-year projection scale for CO₂ sequestration metrics (in metric tons) and translates ecological impact into tradable Carbon Credits.
* **Financial Forecasting Core:** Calculates complete project lifecycle analytics including Initial Setup Capital, Projected 10-Year Maintenance Overhead, Gross Carbon Revenue Yields (₹), and Net Return on Investment (ROI).

---

## 🛠️ Technical Stack & Dependencies

### Frontend Infrastructure
* **Core:** React.js (Hooks, State Management, Controlled Inputs)
* **Styling:** Custom Glassmorphic UI Engineering (`App.css`)
* **Icons:** Lucide-React Component Libraries

### Backend Gateway Architecture
* **Runtime:** Node.js (v18+ recommended) with Express Framework
* **Middleware:** CORS Integration, Native Body-Parser Middleware
* **Process Management:** Secure Asynchronous Sub-process Execution (`child_process.execFile`)

### Machine Learning Core (Python Engine)
* **Execution:** Python 3.9+ Runtime Environments
* **Data Serialization:** Joblib Engine for Model Object Serialization
* **Data Pipelines:** Pandas DataFrames, Numpy Matrix Processors
* **Framework:** Scikit-Learn Predictive Modeling Checkpoints

---

## 💻 Local Installation & Setup Guide

Follow these steps to deploy and configure the environment cluster locally on a Windows/Linux workspace:

### 1. Repository Configuration
```bash
git clone [https://github.com/Asmit45986/GreenMind-AI.git](https://github.com/Asmit45986/GreenMind-AI.git)
cd GreenMind-AI
2. Backend Environment Clustering & Setup
Navigate to the backend directory, install core HTTP nodes, and configure the isolated Python environment:

Bash
cd backend
npm install

# Setup local virtual environment (ai_env) for model evaluation
python -m venv ai_env
source ai_env/bin/activate  # On Windows use: ai_env\Scripts\activate
pip install requirements.txt
Make sure your pre-trained model files (tree_recommender.pkl and survival_regressor.pkl) are correctly placed inside the checkpoints/ directory at the project root.

3. Frontend Configurations
Open a secondary terminal workspace, navigate to the frontend service tier, and install view engines:

Bash
cd frontend
npm install
4. Running the Complete Monorepo Ecosystem
To launch Backend Node Engine (Port 5000): Run npm start or node server.js inside the backend/ directory.

To launch Frontend Interface System: Run npm run dev or npm start inside the frontend/ directory.

🛡️ Production Deployment Specifications
The platform architecture is optimized for cloud scaling and is dynamically configured to handle production states:

Production Environment Flag: Automatic resolution for platform paths via process.env.NODE_ENV === 'production'.

Deployment Runtime Handling: Dynamically targets global Unix engines (python3) during cloud cluster boots (e.g., Render) while preserving paths to local execution binaries (ai_env/Scripts/python.exe) during local prototyping.
