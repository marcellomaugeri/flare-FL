import pickle
from tensorflow.keras.utils import to_categorical
import numpy as np

def load_data(file: str) -> tuple:
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
        features = dict[b'data']
        labels = dict[b'labels']
        
        # Reshape the features to 10000x32x32x3
        features = features.reshape((10000, 3, 32, 32)).transpose(0, 2, 3, 1)
        labels = to_categorical(labels, num_classes=10)
    return features, labels
        
    
def unpickle(file: str) -> dict:
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict
