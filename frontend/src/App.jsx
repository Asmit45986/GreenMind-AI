import React, { useState } from 'react';
import { Leaf, DollarSign, CloudRain, ShieldCheck } from 'lucide-react';
import './App.css';

function App() {
  const [formData, setFormData] = useState({
    vegetation_percentage: 12.5,
    water_nearby: false,
    land_type_enc: 0, // Mapped according to Label Encoder
    soil_type_enc: 3, // Mapped according to Label Encoder
    ph: 7.2,
    moisture: 18.0,
    temperature: 36.5,
    rainfall: 420.0,
    humidity: 30.0,
    aqi: 180,
    elevation: 310.0,
    tree_count: 500
  });

  const [loading, setLoading] = useState(false);
  const [report, setReport] = useState(null);

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : (type === 'select-one' ? parseInt(value) : parseFloat(value) || value)
    }));
  };

  const submitPipeline = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await fetch('http://localhost:5000/api/estimate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          environmental_data: formData,
          tree_count: formData.tree_count
        })
      });
      const resData = await response.json();
      if (resData.success) {
        setReport(resData.data);
      } else {
        alert("Pipeline error occurred!");
      }
    } catch (err) {
      console.error(err);
      alert("Backend Connection Lost! Make sure node server is running on port 5000.");
    }
    setLoading(false);
  };

  return (
    <div className="dashboard-container">
      <div className="header-section">
        <h1>🌲 AI Afforestation Planner</h1>
        <p style={{ color: '#a4b0be', marginTop: '0.5rem' }}>Master Schema Integrated Core Evaluation System</p>
      </div>

      <div className="main-grid">
        <div className="glass-card">
          <h2 style={{ marginTop: 0, borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '0.5rem' }}>⚙️ Input Terrain Parameters</h2>
          <form onSubmit={submitPipeline}>
            <div className="form-group">
              <label>Target Tree Count to Plant</label>
              <input type="number" name="tree_count" className="form-control" value={formData.tree_count} onChange={handleInputChange} />
            </div>
            
            <div className="form-group">
              <label>Land Type Category</label>
              <select name="land_type_enc" className="form-control" value={formData.land_type_enc} onChange={handleInputChange}>
                <option value={0}>Barren Land</option>
                <option value={1}>Rangeland</option>
                <option value={2}>Forest Area</option>
                <option value={3}>Agriculture Zone</option>
                <option value={4}>Urban Patch</option>
              </select>
            </div>

            <div className="form-group">
              <label>Soil Profile Type</label>
              <select name="soil_type_enc" className="form-control" value={formData.soil_type_enc} onChange={handleInputChange}>
                <option value={3}>Sandy Soil</option>
                <option value={1}>Loamy Soil</option>
                <option value={0}>Clayey Soil</option>
                <option value={2}>Rocky Terrain</option>
                <option value={4}>Alluvial Soil</option>
              </select>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
              <div className="form-group">
                <label>Temperature (°C)</label>
                <input type="number" step="0.1" name="temperature" className="form-control" value={formData.temperature} onChange={handleInputChange} />
              </div>
              <div className="form-group">
                <label>Rainfall (mm)</label>
                <input type="number" name="rainfall" className="form-control" value={formData.rainfall} onChange={handleInputChange} />
              </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
              <div className="form-group">
                <label>Air Quality Index (AQI)</label>
                <input type="number" name="aqi" className="form-control" value={formData.aqi} onChange={handleInputChange} />
              </div>
              <div className="form-group">
                <label>Soil pH</label>
                <input type="number" step="0.1" name="ph" className="form-control" value={formData.ph} onChange={handleInputChange} />
              </div>
            </div>

            <div className="form-group" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', margin: '1.5rem 0' }}>
              <input type="checkbox" name="water_nearby" id="water_nearby" checked={formData.water_nearby} onChange={handleInputChange} />
              <label htmlFor="water_nearby" style={{ margin: 0, cursor: 'pointer' }}>Water Source Nearby Available</label>
            </div>

            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? "⚡ Running ML Matrix Loop..." : "🚀 Generate Full Projection"}
            </button>
          </form>
        </div>

        <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', justifyItems: 'center' }}>
          <h2 style={{ marginTop: 0, borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '0.5rem' }}>📊 ML Analytics Output</h2>
          
          {!report ? (
            <div style={{ textAlign: 'center', margin: 'auto', color: '#a4b0be' }}>
              <Leaf size={48} style={{ opacity: 0.3, marginBottom: '1rem' }} />
              <p>Fill features and trigger pipeline execution matrix.</p>
            </div>
          ) : (
            <div>
              <div style={{ padding: '1rem', background: 'rgba(46, 204, 113, 0.1)', borderRadius: '8px', marginBottom: '1.5rem' }}>
                <h3 style={{ margin: '0 0 0.5rem 0', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <ShieldCheck color="#2ecc71" /> ML Model Core Prediction
                </h3>
                <div className="metric-row"><span>Recommended Tree:</span> <span className="metric-value">{report.prediction.recommended_tree}</span></div>
                <div className="metric-row"><span>Confidence Score:</span> <span>{report.prediction.confidence_score}</span></div>
                <div className="metric-row"><span>Survival Probability:</span> <span>{report.prediction.survival_probability}</span></div>
              </div>

              <div style={{ padding: '1rem', background: 'rgba(52, 152, 219, 0.1)', borderRadius: '8px', marginBottom: '1.5rem' }}>
                <h3 style={{ margin: '0 0 0.5rem 0', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <CloudRain color="#3498db" /> Carbon Offset Analytics
                </h3>
                <div className="metric-row"><span>Estimated Active Survival:</span> <span>{report.environmental_impact.active_trees_survived}</span></div>
                <div className="metric-row"><span>CO₂ Stored (10 Years):</span> <span className="metric-value">{report.environmental_impact.total_co2_sequestration_tons} Tons</span></div>
                <div className="metric-row"><span>Carbon Credits Earned:</span> <span>{report.environmental_impact.carbon_credits_earned} Credits</span></div>
              </div>

              <div style={{ padding: '1rem', background: 'rgba(241, 196, 15, 0.1)', borderRadius: '8px' }}>
                <h3 style={{ margin: '0 0 0.5rem 0', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <DollarSign color="#f1c40f" /> Financial Economics
                </h3>
                <div className="metric-row"><span>Initial Setup Cost:</span> <span>{report.financial_analytics.initial_setup_cost}</span></div>
                <div className="metric-row"><span>Total Project Cost:</span> <span>{report.financial_analytics.total_maintenance_cost}</span></div>
                <div className="metric-row"><span>Est. Carbon Revenue:</span> <span className="metric-value" style={{ color: '#2ecc71' }}>{report.financial_analytics.estimated_gross_revenue}</span></div>
                <div className="metric-row"><span>Net ROI Return (₹):</span> <span className="metric-value">{report.financial_analytics.net_financial_return}</span></div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;