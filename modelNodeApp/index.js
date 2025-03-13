const express = require("express");
const tf = require("@tensorflow/tfjs-node");

const app = express();
app.use(express.json());

let model;

// Load the model
(async () => {
    console.log("test");
    const modelPath = path.resolve(__dirname, 'normalized_model_54299/model.json');
    const modelUrl = `file://${modelPath}`;
    model = await tf.loadLayersModel(modelUrl);
    console.log("Model loaded successfully.");
})();

app.post("/predict", async (req, res) => {
    try {
        if (!model) {
            return res.status(500).json({ error: "Model not loaded yet" });
        }
        
        const inputData = tf.tensor2d([req.body.input]);
        const prediction = model.predict(inputData);
        const result = await prediction.data();
        
        res.json({ prediction: Array.from(result) });
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
});

const PORT = 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
