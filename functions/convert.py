import onnxmltools
from tensorflow.keras.models import load_model

model = load_model("best_model1.keras")

onnx_model = onnxmltools.convert_keras(model) 

onnxmltools.utils.save_model(onnx_model, 'keras_example.onnx')