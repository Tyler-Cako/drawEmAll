import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.preprocessing.image import ImageDataGenerator

#Creates a model with preset layers, returns a build CNN model
#Parameters: dropout=0.45, grayscale = False,image_size = 128, optimizer = 'adam'
def create_CNN_model(dropout=0.45, grayscale = False, image_size = 128, optimizer = 'adam'):
    model = models.Sequential()
    if grayscale:
        model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(image_size, image_size, 1)))
    else:
        model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(image_size, image_size, 3)))
    model.add(layers.BatchNormalization()) # does something good, maybe i'll read more about it but i just added it and it helped a lot
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))

    model.add(layers.Flatten())#1d for neural network

    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dropout(dropout)) #address overfitting this helps reduce over fitting
    model.add(layers.Dense(3, activation='softmax'))

    model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
              metrics=['accuracy'])

    return model


#Trains the model returns the model with the highest accuracy on the test data
#Parameters: model,model,X_train,y_train,X_test,y_test, num_epochs=75, batch_s = 32, save_path = './models/best_model_func.keras'
def CNN_fit_train(model,X_train,y_train,X_test,y_test, num_epochs=75, num_batch = 32, save_path = './models/best_model_func.keras', datagen = False):


    checkpoint = ModelCheckpoint(save_path, 
                             monitor='val_accuracy',    # Monitor validation accuracy
                             save_best_only=True,       # Save only the best weights
                             mode='max',                # 'max' means we want to maximize the metric
                             verbose=1)
    if datagen:
        gen = ImageDataGenerator(
            rotation_range=20,              # Randomly rotate images by up to x degrees
            width_shift_range=0.2,          # Randomly shift images horizontally by x%
            height_shift_range=0.2,         # Randomly shift images vertically by x%
            shear_range=0.2,                # Apply shear transformations
            zoom_range=0.2,                 # Random zoom
            horizontal_flip=True,           # Randomly flip images horizontally
            fill_mode='nearest'             # Strategy for filling in missing pixels (due to rotation or shift)
        )

        gen.fit(X_train)
        model.fit(gen.flow(X_train, y_train, batch_size=num_batch), 
                        epochs=num_epochs, 
                        validation_data=(X_test, y_test),
                        callbacks= [checkpoint])
    else:
        model.fit(X_train, y_train, 
                epochs=num_epochs, 
                batch_size=num_batch, 
                validation_data=(X_test, y_test),
                callbacks= [checkpoint])
    return tf.keras.models.load_model(save_path)


def CNN_accuracy(model, X_test, y_test):
    pred_probs = model.predict(X_test)
    predicted_class = np.argmax(pred_probs, axis=1)
    acc = np.mean(predicted_class == y_test)
    return acc

def load_CNN_model(path = './models/best_model_func.keras'):
    return tf.keras.models.load_model(path)