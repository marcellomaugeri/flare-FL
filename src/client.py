import argparse
from models.cifar10 import get_model
import pickle
import numpy as np
from utils.cifar10_utils import load_data
from model_validation_api_client import Client
from model_validation_api_client.models import PostValidateModelBody, PostValidateModelBodyModel, PostValidateModelResponse200
from model_validation_api_client.api.default import post_validate_model
from model_validation_api_client.types import Response, Unset
import base64

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

# Evaluate the model
#loss, accuracy = model.evaluate(test_features, test_labels)

# Save the weights
model.save_weights('data/cifar10/cifar10_weights.weights.h5')

# Load the weights
model.load_weights('data/cifar10/cifar10_weights.weights.h5')

if args.validate:
    # Evaluate the model
    client = Client("http://localhost:8080")
    
    # load the weights from the file and encode them in base64
    with open('data/cifar10/cifar10_weights.weights.h5', 'rb') as f:
        weights = base64.b64encode(f.read()).decode('utf-8')    
        
    request_data : PostValidateModelBody = PostValidateModelBody(model=PostValidateModelBodyModel.CIFAR10, weights=weights)
    response : Response = post_validate_model.sync_detailed(client=client, body=request_data)
        
    if isinstance(response.parsed, PostValidateModelResponse200):
        if isinstance(response.parsed.error, Unset):
            print("Model validation successful")
        else:
            print("Model validation failed")