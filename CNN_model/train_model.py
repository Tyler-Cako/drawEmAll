import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import ModelCheckpoint


#Creates a model with preset layers, returns a build CNN model
#Parameters: dropout=0.45, grayscale = False
def create_CNN_model(dropout=0.45, grayscale = False, image_size = 128):
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
    model.add(layers.Dropout(dropout)) #address overfitting
    model.add(layers.Dense(3, activation='softmax'))

    model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
              metrics=['accuracy'])

    return model


#Trains the model returns the model with the highest accuracy on the test data
#Parameters: model,model,X_train,y_train,X_test,y_test, num_epochs=75, batch_s = 32
def train(model,X_train,y_train,X_test,y_test, num_epochs=75, batch_s = 32):

    checkpoint = ModelCheckpoint('./models/best_model_func.keras', 
                             monitor='val_accuracy',    # Monitor validation accuracy
                             save_best_only=True,       # Save only the best weights
                             mode='max',                # 'max' means we want to maximize the metric
                             verbose=1)
    history = model.fit(X_train, y_train, 
                    epochs=num_epochs, 
                    batch_s=32, 
                    validation_data=(X_test, y_test),
                    callbacks= [checkpoint])
    
    return tf.keras.models.load_model('./models/best_model_func.keras')




