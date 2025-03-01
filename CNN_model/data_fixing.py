import os
from PIL import Image
import numpy as np
from sklearn.model_selection import train_test_split


#Formats images and saves them as numpy arrays, according to parameters, returns (images,labels)
# Pokemonn featuer numbers
# "Bulbasaur": 0,
# "Charmander": 1,
# "Squirtle": 2,
#Parameters folder_dir = '../images/dataset', image_size = 128, grayscale = False
def format_and_label_data(folder_dir = '../images/dataset', image_size = 128, grayscale = False, combined = False, save_path='../images_as_npz/gen_1_formatted_images.npz'):
#test push
    image_data = []
    labels = []
    grayscale_data = []

    pokemon_to_feature_num = {}
    pokemon_folders = [d for d in os.listdir(folder_dir) if os.path.isdir(os.path.join(folder_dir, d))]

    # Assign a numerical label to each Pokémon
    for index, pokemon in enumerate(pokemon_folders):
        pokemon_to_feature_num[pokemon] = index

    for pokemon in pokemon_folders:
        pokemon_folder = os.path.join(folder_dir, pokemon)
        
        for filename in os.listdir(pokemon_folder):
            if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith('.jfif'):
                image_path = os.path.join(pokemon_folder, filename)
                
                # Open the image and resize it to a fixed size 
                img = Image.open(image_path).resize((image_size, image_size))
                if combined:  # Generate both grayscale and RGB
                        # garayscasle
                        grayscale_img = img.convert('L')
                        grayscale_array = np.array(grayscale_img)

                        if img.mode == 'RGBA':
                            img = img.convert('RGB')  
                        rgb_array = np.array(img)

                        if grayscale_array.shape == (image_size, image_size) and rgb_array.shape == (image_size, image_size, 3):
                            grayscale_data.append(grayscale_array.reshape(image_size, image_size, 1))  # Add channel dimension
                            image_data.append(rgb_array)
                            labels.append(pokemon_to_feature_num[pokemon])
                #grayscale
                elif grayscale:
                    img = img.convert('L')  
                    img_array = np.array(img)
            
                    if img_array.shape != (image_size, image_size):
                        print(f"Skipping {filename}, invalid shape: {img_array.shape}")
                        continue
                    else:
                        image_data.append(img_array)
                        labels.append(pokemon_to_feature_num[pokemon])

                else:
                # Convert to RGB if it's RGBA
                    if img.mode == 'RGBA':
                        img = img.convert('RGB')  # Discard the alpha channel
                    img_array = np.array(img)
            
                    if img_array.shape != (image_size, image_size, 3):
                        print(f"Skipping {filename}, invalid shape: {img_array.shape}")
                        continue
                    else:
                        image_data.append(img_array)
                        labels.append(pokemon_to_feature_num[pokemon])
        
    labels = np.array(labels, dtype=np.int32)
    image_data = np.array(image_data, dtype=np.uint8)
    grayscale_data = np.array(grayscale_data, dtype=np.uint8)
    if grayscale:

        save_path = f'../images_as_npz/pokemon_grayscale_{image_size}x{image_size}.npz'
        np.savez_compressed(save_path, grayscale_images=grayscale_data, labels=labels)
    elif combined:
        save_path = f'../images_as_npz/pokemon_combined_{image_size}x{image_size}.npz'
        np.savez_compressed(save_path, images=image_data, grayscale_images=grayscale_data, labels=labels)
    else:

        save_path = f'../images_as_npz/pokemon_rgb_non_norm{image_size}x{image_size}.npz'
        np.savez_compressed(save_path, images=image_data, labels=labels)

    print(f"Dataset saved at {save_path}")

    if combined:
        return grayscale_data, image_data, labels
    else:
        return (image_data, labels)


def format_image(image_path = '../images/Hand_Drawn/Bulbasaur/bulb_color.png', grayscale = False, image_size = 128):
    img = Image.open(image_path).resize((image_size, image_size))
    #grayscale
    if grayscale:
        img = img.convert('L')  
        img_array = np.array(img)

        if img_array.shape != (image_size, image_size):

            print("invalid image shape")
            return None
        else:
            return img_array

    else:
    # Convert to RGB if it's RGBA
        if img.mode == 'RGBA':
            img = img.convert('RGB')  # Discard the alpha channel
        img_array = np.array(img)

        if img_array.shape != (image_size, image_size, 3):
            print('invalid shape')
            return None
        else:
            return img_array
    pass