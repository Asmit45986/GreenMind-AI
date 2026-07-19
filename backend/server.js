const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const { execFile } = require('child_process'); // Using execFile instead of exec
const path = require('path');
const fs = require('fs');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(bodyParser.json());

app.post('/api/estimate', (req, res) => {
    const { environmental_data, tree_count } = req.body;
    const count = tree_count || 500;

    const projectRoot = path.resolve(__dirname, '..');
    const bridgeScript = path.join(projectRoot, 'backend', 'bridge_controller.py');
    const venvPython = path.join(projectRoot, 'ai_env', 'Scripts', 'python.exe');
    
    const inputPayload = {
        environmental_data: environmental_data,
        tree_count: count
    };
    
    const tempFilePath = path.join(__dirname, 'temp_input.json');
    fs.writeFileSync(tempFilePath, JSON.stringify(inputPayload));

    console.log(`Executing via execFile: ${venvPython}`);
    console.log(`Arguments: [${bridgeScript}, ${tempFilePath}]`);

    // 💡 execFile runs the executable directly without creating a shell, 
    // which completely ignores spaces and escaping issues in Windows!
    execFile(venvPython, [bridgeScript, tempFilePath], { cwd: projectRoot }, (error, stdout, stderr) => {
        // Safe check: Always cleanup the temp file
        if (fs.existsSync(tempFilePath)) fs.unlinkSync(tempFilePath);

        if (error) {
            console.error(`Execution Error: ${error.message}`);
            return res.status(500).json({ 
                success: false, 
                error: `Python Exec Failure: ${error.message}. Stderr: ${stderr || 'None'}` 
            });
        }
        
        try {
            const ml_response = JSON.parse(stdout.trim());
            if (ml_response.status === "error") {
                return res.status(500).json({ success: false, error: ml_response.message });
            }
            return res.status(200).json({ success: true, data: ml_response });
        } catch (parseErr) {
            console.error(`Parsing failure. Raw Output: ${stdout}`);
            return res.status(500).json({ success: false, error: `JSON Parse Fail: ${stdout}` });
        }
    });
});

app.listen(PORT, () => {
    console.log(`Server running on port http://localhost:${PORT}`);
});