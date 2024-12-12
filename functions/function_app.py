import logging
import io
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model

import azure.functions as func
import azurefunctions.extensions.bindings.blob as blob

app = func.FunctionApp()

# @app.blob_trigger(
#     arg_name="client", path="trainingblobs/{foldername}/{blobname}.png", connection="AzureWebJobsStorage"
# )
# def blob_trigger(client: blob.BlobClient):
@app.route(methods=[func.HttpMethod.POST], auth_level=func.AuthLevel.ANONYMOUS)
def predict_pokemon(req: func.HttpRequest):
    logging.info(
        f"Python blob trigger function processed blob \n"
    )

    model = load_model("best_model1.keras")
    pokemon_map = {
        0: "Bulbasaur",
        1: "Charmander",
        2: "Squirtle"
    }

    stream = io.BytesIO()

    blob = io.BytesIO(req.get_body());

    #num_bytes = client.download_blob().readinto(stream)
    #image = Image.open(stream).convert("RGB").resize((128, 128))

    image = Image.open(blob).convert("RGB").resize((128, 128))
    img_array = np.array(image)
    img_array = np.array([img_array])

    if img_array.shape != (1, 128, 128, 3):
        func.HttpResponse("Wrong array shape.", status_code=400)

    pred_probs = model.predict(img_array)
    print(f"pred_probs: {pred_probs}")
    predicted_class = np.argmax(pred_probs[0])
    print(f"predicted_class: {predicted_class}")
    predicted_pokemon = pokemon_map[predicted_class]
    print(f"predicted_pokemon: {predicted_pokemon}")

    #print(f"pred_probs: {pred_probs} \n pred_class: {predicted_class} \n pred_pokemon: {predicted_pokemon}")

    return func.HttpResponse(f"{predicted_pokemon}", status_code=200)
