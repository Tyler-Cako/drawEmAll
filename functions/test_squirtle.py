import io
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model

model = load_model("best_model1.keras")
pokemon_map = {
    0: "Bulbasaur",
    1: "Charmander",
    2: "Squirtle"
}

image = Image.open("squirtle.png").convert("RGB").resize((128, 128))
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
