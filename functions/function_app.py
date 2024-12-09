import logging
import io
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model

import azure.functions as func
import azurefunctions.extensions.bindings.blob as blob

app = func.FunctionApp()

@app.blob_trigger(
    arg_name="client", path="trainingblobs/{foldername}/{blobname}.png", connection="AzureWebJobsStorage"
)
def blob_trigger(client: blob.BlobClient):
    logging.info(
        f"Python blob trigger function processed blob \n"
    )

    model = load_model("best_model1.keras")

    hand_data = []
    stream = io.BytesIO()
    num_bytes = client.download_blob().readinto(stream)
    image = Image.open(stream).convert("RGB").resize((128, 128))
    img_array = np.array(image)
    img_array = np.array([img_array])

    if img_array.shape == (128, 128, 3):
        return


    pred_probs = model.predict(img_array)
    predicted_class = np.argmax(pred_probs, axis=1)

    print(f"pred_probs: {pred_probs} \n pred_class: {predicted_class}")
