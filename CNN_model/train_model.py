import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Model
from tensorflow.keras import Input
#Creates a model with preset layers, returns a build CNN model
#Parameters: dropout=0.45, grayscale = False,image_size = 128, optimizer = 'adam'
def create_CNN_model(dropout=0.25, grayscale=False, image_size=128, num_classes=3, optimizer='adam'):
    model = models.Sequential()
    # model.add(layers.Rescaling(1./255, input_shape=(image_size, image_size, 3)))  # Rescaling layer
    if grayscale:
        model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(image_size, image_size, 1)))
    else:
        model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(image_size, image_size, 3)))
    
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling2D((2, 2)))

    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling2D((2, 2)))

    model.add(layers.Conv2D(128, (3, 3), activation='relu'))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling2D((2, 2)))

    model.add(layers.Conv2D(128, (3, 3), activation='relu'))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling2D((2, 2)))

    # model.add(layers.Flatten())
    model.add(layers.GlobalAveragePooling2D())
    
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dropout(dropout))
    
    # Adjust the output layer to match the number of classes
    model.add(layers.Dense(num_classes, activation='softmax'))

    model.compile(optimizer=optimizer,
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
                  metrics=['accuracy'])

    return model


#Trains the model returns the model with the highest accuracy on the test data
#Parameters: model,model,X_train,y_train,X_test,y_test, num_epochs=75, batch_s = 32, save_path = './models/best_model_func.keras'
def CNN_fit_train(model,X_train,y_train,X_test,y_test, num_epochs=75, num_batch = 32, save_path = './models/best_model_func.keras', datagen = False,combined = False ):


    checkpoint = ModelCheckpoint(save_path, 
                             monitor='val_accuracy',    # Monitor validation accuracy
                             save_best_only=True,       # Save only the best weights
                             mode='max',                # 'max' means we want to maximize the metric
                             verbose=1)
    
    if datagen:

        gen = ImageDataGenerator(
            rescale=1./255, # rescales 
            rotation_range=20,       # Randomly rotate images by up to x degrees
            width_shift_range=0.2,          # Randomly shift images horizontally by x%
            height_shift_range=0.2,         # Randomly shift images vertically by x%
            shear_range=0.2,                # Apply shear transformations
            zoom_range=0.2,                 # Random zoom
            horizontal_flip=True,           # Randomly flip images horizontally
            fill_mode='nearest'             # Strategy for filling in missing pixels (due to rotation or shift)
        )
        val_gen = ImageDataGenerator(rescale=1./255)
        # gen.fit(X_train)
        model.fit(gen.flow(X_train, y_train, batch_size=num_batch), 
                        epochs=num_epochs, 
                        validation_data=val_gen.flow(X_test, y_test, batch_size=32),
                        callbacks= [checkpoint])
    elif combined:
        model.fit(
            [ X_train["rgb"],  X_train["grayscaled"]], y_train, 
            epochs=75, 
            batch_size=32, 
            validation_data=([ X_test["rgb"],  X_test["grayscaled"]], y_test),
            callbacks=[checkpoint]
        )
    else:
        model.fit(X_train, y_train, 
                epochs=num_epochs, 
                batch_size=num_batch, 
                validation_data=(X_test, y_test),
                callbacks= [checkpoint])
    return tf.keras.models.load_model(save_path)



def create_combined_CNN_model(dropout=0.45,  image_size = 128, optimizer = 'adam'):
    # rgb
    rgb_input = Input(shape=(128, 128, 3), name="rgb_input")
    x_rgb = layers.Conv2D(32, (3, 3), activation='relu')(rgb_input)
    x_rgb = layers.BatchNormalization()(x_rgb)
    x_rgb = layers.MaxPooling2D((2, 2))(x_rgb)
    x_rgb = layers.Conv2D(32, (3, 3), activation='relu')(x_rgb)
    x_rgb = layers.MaxPooling2D((2, 2))(x_rgb)
    x_rgb = layers.Conv2D(32, (3, 3), activation='relu')(x_rgb)
    x_rgb = layers.MaxPooling2D((2, 2))(x_rgb)
    x_rgb = layers.Flatten()(x_rgb)

    # grayscale
    grayscale_input = Input(shape=(128, 128, 1), name="grayscale_input")
    x_gray = layers.Conv2D(32, (3, 3), activation='relu')(grayscale_input)
    x_gray = layers.BatchNormalization()(x_gray)
    x_gray = layers.MaxPooling2D((2, 2))(x_gray)
    x_gray = layers.Conv2D(32, (3, 3), activation='relu')(x_gray)
    x_gray = layers.MaxPooling2D((2, 2))(x_gray)
    x_gray = layers.Conv2D(32, (3, 3), activation='relu')(x_gray)
    x_gray = layers.MaxPooling2D((2, 2))(x_gray)
    x_gray = layers.Flatten()(x_gray)

    # come bnranches
    combined = layers.Concatenate()([x_rgb, x_gray])
    x_combined = layers.Dense(64, activation='relu')(combined)

    x_combined = layers.Dense(64, activation='relu')(x_combined)
    x_combined = layers.Dropout(dropout)(x_combined)
    output = layers.Dense(3, activation='softmax', name="output")(x_combined)

    # Create the Model
    model = Model(inputs=[rgb_input, grayscale_input], outputs=output)

    # Compile the Model
    model.compile(optimizer=optimizer,
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(),
                  metrics=['accuracy'])

    return model

def CNN_accuracy(model, X_test, y_test):
    pred_probs = model.predict(X_test)
    predicted_class = np.argmax(pred_probs, axis=1)
    acc = np.mean(predicted_class == y_test)
    return acc
def combined_CNN_acc(model, gray,rgb,y_test):
    pred_probs = model.predict([rgb,gray])
    predicted_class = np.argmax(pred_probs, axis=1)
    acc = np.mean(predicted_class == y_test)
    return acc
def load_CNN_model(path = './models/best_model_func.keras'):
    return tf.keras.models.load_model(path)

def CNN_one_pred(model, image):
    class_to_pokemon = {
        0 : "Bulbasaur",
        1 : "Charmander",
        2 : "Squirtle",

    }
    image = np.expand_dims(image, axis=0)
    pred_probs = model.predict(image)
    predicted_class = np.argmax(pred_probs, axis=1)
    poke = class_to_pokemon[predicted_class[0]]
    return poke

def layer_visualization(cnn_model):
    layer_outputs = [layer.output for layer in cnn_model.layers if isinstance(layer, layers.Conv2D)]

    visualization_model = Model(inputs=cnn_model.input, outputs=layer_outputs)
    return visualization_model
    pass