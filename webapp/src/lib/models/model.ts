import { loadLayersModel, type LayersModel } from '@tensorflow/tfjs-node';
import path from 'path';

import { fileURLToPath } from 'url';

// Manually define __dirname
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const modelPath = path.resolve(__dirname, './normalized_model_54299/model.json');
const modelUrl = `file://${modelPath}`;

export async function loadModel() {
    try {
        const model = await loadLayersModel(modelUrl); 
        if (model == undefined) throw new Error("Failed to load model");
        console.log("Model loaded successfully");
        return model as LayersModel;
    } catch (error) {
        console.error("Model failed to load: ", error);
    }
};