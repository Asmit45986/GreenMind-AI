const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const { execFile } = require('child_process'); 
const path = require('path');
const fs = require('fs');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(bodyParser.json());

app.post('/api/estimate', (req, res) => {
    // 🔥 FIXED: Direct req.body pass kar rahe hain jo already structured hai frontend se
    const inputPayload = req.body;
    
    const projectRoot = path.resolve(__dirname, '..');
    const bridgeScript = path.join(projectRoot, 'backend', 'bridge_controller.py');
    
    const isProduction = process.env.NODE_ENV === 'production' || !fs.existsSync(path.join(projectRoot, 'ai_env'));
    
    const venvPython = isProduction 
        ? 'python3' 
        : path.join(projectRoot, 'ai_env', 'Scripts', 'python.exe');
    
    const tempFilePath = path.join(__dirname, 'temp_input.json');
    fs.writeFileSync(tempFilePath, JSON.stringify(inputPayload));

    execFile(venvPython, [bridgeScript, tempFilePath], { cwd: projectRoot }, (error, stdout, stderr) => {
        if (fs.existsSync(tempFilePath)) fs.unlinkSync(tempFilePath);

        if (error) {
            console.error(`Execution Error: ${error.message}`);
            return res.status(500).json({ 
                success: false, 
                error: `Python Exec Failure: ${error.message}` 
            });
        }
        
        try {
            const ml_response = JSON.parse(stdout.trim());
            if (ml_response.status === "error") {
                return res.status(500).json({ success: false, error: ml_response.message });
            }
            return res.status(200).json({ success: true, data: ml_response });
        } catch (parseErr) {
            return res.status(500).json({ success: false, error: `JSON Parse Fail: ${stdout}` });
        }
    });
});

app.listen(PORT, () => {
    console.log(`Server running on port http://localhost:${PORT}`);
});