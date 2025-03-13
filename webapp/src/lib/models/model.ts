import * as tf from '@tensorflow/tfjs';
import path from 'path';

import { fileURLToPath } from 'url';

// Manually define __dirname
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const modelPath = path.resolve(__dirname, './normalized_model_54299/model.json');
const modelUrl = `file://${modelPath}`;

let model: tf.LayersModel | null = null;

export async function loadModel() {
    try {
        const model = await tf.loadLayersModel(modelUrl); 
        console.log("Model loaded successfully");
        return model;
    } catch (error) {
        console.error("Model failed to load: ", error);
    }
};

export function getModel(): tf.LayersModel | null {
    return model;
}