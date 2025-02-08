import argparse
from models.cifar10 import get_model
import numpy as np
from utils.cifar10_utils import load_data
from model_validation_api_client import Client
from model_validation_api_client.models import GetValidateModelModel, GetValidateModelResponse200
from model_validation_api_client.api.default import get_validate_model
from model_validation_api_client.types import Response, Unset
import os

parser = argparse.ArgumentParser(description='Train a model.')
parser.add_argument('--data-path', type=str, default='data/cifar10/data_batch_1', help='Path to the training data')
parser.add_argument('--validate', action='store_true', help='Validate the model after training')
args = parser.parse_args()
model = get_model()

# Load the CIFAR-10 dataset
features, labels = load_data('data/cifar10/data_batch_1')

# Train the model
model.fit(features, labels, epochs=1, batch_size=32)

# Load the test data
test_features, test_labels = load_data('data/cifar10/test_batch')

weights_file = 'data/cifar10/cifar10_weights.weights.h5'

model.save_weights(weights_file)

if args.validate:
    # Evaluate the model
    client = Client("http://localhost:8080")
    
    # load the weights from the file and encode them in base64
    #with open(weights_file, 'rb') as f:
    #    weights = f.read()
    
    #Get the absolute path of the weights file
    weights = os.path.abspath(weights_file) 
     
    response : Response = get_validate_model.sync_detailed(client=client, model=GetValidateModelModel.CIFAR10, weights=weights)
    
    if isinstance(response.parsed, GetValidateModelResponse200):
        if isinstance(response.parsed.error, Unset):
            print("Model validation successful")
        else:
            print("Model validation failed")