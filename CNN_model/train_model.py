import numpy as np
# from sklearn.model_selection import train_test_split
from augment import rotate, translate_x, translate_y, shear_x, shear_y, RandAugment
import math
import tensorflow as tf
import scipy.ndimage as ndimage
from keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.models import Model
from tensorflow.keras import layers, Input
from tensorflow.keras.preprocessing.image import ImageDataGenerator
# from tensorflow.tfm.vision.augment import rotate
#Creates a model with preset layers, returns a build CNN model
#Parameters: dropout=0.45, grayscale = False,image_size = 128, optimizer = 'adam'
def create_CNN_model(dropout=0.3, grayscale=False, image_size=128, num_classes=3, optimizer='adam'):
    model = models.Sequential()
    if grayscale:
        model.add(layers.InputLayer(input_shape=(image_size, image_size, 1)))
    else:
        model.add(layers.InputLayer(input_shape=(image_size, image_size, 3)))

    # model.add(layers.Rescaling(1./255))
    # model.add(layers.RandomRotation(factor=(-0.2, 0.2), fill_mode='nearest', interpolation='bilinear'))
    # model.add(layers.RandomZoom(height_factor=0.2, width_factor=0.2, fill_mode='nearest'))
    # model.add(layers.RandomTranslation(height_factor=0.2, width_factor=0.2, fill_mode='nearest'))
    # model.add(layers.RandomFlip("horizontal"))
    # # model.add(layers.RandomBrightness(factor=0.2))
    # model.add(layers.RandomContrast(factor=0.2))


    model.add(layers.Conv2D(32, (3, 3) ))
    model.add(layers.BatchNormalization())  
    model.add(layers.ReLU())  
    model.add(layers.MaxPooling2D((2, 2)))

    model.add(layers.Conv2D(64, (3, 3) ))
    model.add(layers.BatchNormalization())
    model.add(layers.ReLU())  
    model.add(layers.MaxPooling2D((2, 2)))

    model.add(layers.Conv2D(128, (3, 3)))
    model.add(layers.BatchNormalization())
    model.add(layers.ReLU())  
    model.add(layers.MaxPooling2D((2, 2)))

    model.add(layers.Conv2D(128, (3, 3)))
    model.add(layers.BatchNormalization())
    model.add(layers.ReLU())  
    model.add(layers.MaxPooling2D((2, 2)))

    # model.add(layers.Flatten())
    model.add(layers.GlobalAveragePooling2D())
    
    model.add(layers.Dense(128))
    model.add(layers.BatchNormalization())
    model.add(layers.ReLU())  
    model.add(layers.Dropout(dropout))
    
    # Adjust the output layer to match the number of classes
    model.add(layers.Dense(num_classes, activation='softmax'))

    model.compile(optimizer=optimizer,
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
                  metrics=['accuracy'])

    return model

def CNN_tsData_train(model, train_dataset, val_dataset, class_weights = {}, num_epochs=75, save_path = './models/best_model_func.keras'):
    checkpoint = ModelCheckpoint(save_path, 
                             monitor='val_loss',    # Monitor validation loss
                             save_best_only=True,    # Save only the best weights
                             mode='min',             # 'min' because we want to minimize the loss
                             verbose=1)
    early_stopping = EarlyStopping(monitor='val_loss', patience=15, restore_best_weights=True)

    model.fit(train_dataset, 
            epochs=num_epochs,  
            validation_data=val_dataset,
            class_weight = class_weights,
            callbacks= [checkpoint, early_stopping])
    return model

def augment_train(image, label):
    image = tf.cast(image, tf.float32) / 255.0
    
    # Apply augmentations
 
    image = tf.image.random_flip_left_right(image)
    image = tf.image.random_flip_up_down(image)

    image = rotate(image, tf.random.uniform([], -30, 30))

    image = tf.image.random_contrast(image, 0.8, 1.2)  # Random contrast adjustment
    image = tf.image.random_brightness(image, 0.8, 1.2)  # Random brightness adjustmen
    
    return image, label

def augment_val(image, label):
    image = tf.cast(image, tf.float32) / 255.0
    return image, label
def create_augmented_train_val_datasets(X_train, y_train, X_test, y_test):
    
    train_dataset = tf.data.Dataset.from_tensor_slices((X_train, y_train))
    val_dataset = tf.data.Dataset.from_tensor_slices((X_test, y_test))

    train_dataset = train_dataset.shuffle(300)
    

    train_dataset = train_dataset.map(augment_train, num_parallel_calls=1)
    val_dataset = val_dataset.map(augment_val, num_parallel_calls=1)
    
    train_dataset = train_dataset.batch(8)  # batch sizew
    train_dataset = train_dataset.prefetch(1)  

    val_dataset = val_dataset.batch(8)
    val_dataset = val_dataset.cache()
    val_dataset = val_dataset.prefetch(1)

    return train_dataset, val_dataset
#Trains the model returns the model with the highest accuracy on the test data
#Parameters: model,model,X_train,y_train,X_test,y_test, num_epochs=75, batch_s = 32, save_path = './models/best_model_func.keras'
def CNN_fit_train(model,X_train,y_train,X_test,y_test, class_weights = {}, num_epochs=75, num_batch = 32, save_path = './models/best_model_func.keras', datagen = False,combined = False):


    # checkpoint = ModelCheckpoint(save_path, 
    #                          monitor='val_accuracy',    # Monitor validation accuracy
    #                          save_best_only=True,       # Save only the best weights
    #                          mode='max',                # 'max' means we want to maximize the metric
    #                          verbose=1)
    #monitor val_loss
    checkpoint = ModelCheckpoint(save_path, 
                             monitor='val_loss',    # Monitor validation loss
                             save_best_only=True,    # Save only the best weights
                             mode='min',             # 'min' because we want to minimize the loss
                             verbose=1)
    image_gen = ImageDataGenerator(rotation_range=30, # rotate the image 30 degrees
                               width_shift_range=0.2, # Shift the pic width by a max of 20%
                               height_shift_range=0.2, # Shift the pic height by a max of 20%
                               rescale=1/255, # Rescale the image by normalzing it.
                               shear_range=0.2, # Shear means cutting away part of the image (max 20%)
                               zoom_range=0.2, # Zoom in by 20% max
                               horizontal_flip=True, # Allo horizontal flipping
                               fill_mode='nearest' # Fill in missing pixels with the nearest filled value
                              )

    if datagen:
        early_stopping = EarlyStopping(monitor='val_loss', patience=15, restore_best_weights=True)

        # model.fit(X_train, y_train, 
        #         epochs=num_epochs, 
        #         batch_size=num_batch, 
        #         validation_data=(X_test, y_test),
        #         callbacks= [checkpoint, early_stopping])
        train_data = image_gen.flow(X_train, y_train, num_batch)

        test_gen = ImageDataGenerator(rescale=1/255)

        # Use the generator to preprocess your test data
        test_data = test_gen.flow(X_test, y_test, batch_size=num_batch)
        model.fit(train_data ,
                epochs=num_epochs, 
                batch_size=num_batch, 
                validation_data=test_data,
                callbacks= [checkpoint, early_stopping])

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
    return model



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