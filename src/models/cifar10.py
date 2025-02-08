import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

def get_model() -> tf.keras.Model:
    model = Sequential()

    # --- Reduced Convolutional Block ---
    model.add(layers.Conv2D(16, (3, 3), padding='same', activation='relu', input_shape=(32, 32, 3)))
    #model.add(layers.BatchNormalization()) # Optional: Add back if needed
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))
    model.add(layers.Dropout(0.25))  # Keep dropout, but adjust rate

    # --- Potentially add a *second* simplified block (Experiment) ---
    #Uncommenting the following lines we can add a second conv layer
    #model.add(layers.Conv2D(32, (3, 3), padding='same', activation='relu'))
    ##model.add(layers.BatchNormalization())
    #model.add(layers.MaxPooling2D(pool_size=(2, 2)))
    #model.add(layers.Dropout(0.25))

    # --- Flatten and Dense Layers ---
    model.add(layers.Flatten())
    model.add(layers.Dense(32, activation='relu')) # Reduced dense layer size
    #model.add(layers.BatchNormalization()) #Optional
    model.add(layers.Dropout(0.5)) # Keep dropout
    model.add(layers.Dense(10, activation='softmax'))

    # Compiling the model
    model.compile(optimizer='adam', loss="categorical_crossentropy", metrics=['accuracy'])
    
    # Checking the model summary
    #model.summary()

    return model