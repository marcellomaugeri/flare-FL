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
parser.add_argument('--train', action='store_true', help='Enable training (disabled because of the precomputed weights)')
args = parser.parse_args()

if not args.train and not args.validate:
    print("Both training and validation are disabled, is it intended?")

index = args.data_path[-1]
weights_file = f'data/cifar10/precomputed/precomputed_{index}.weights.h5'

if args.train:
    model = get_model()

    # Load the CIFAR-10 dataset
    features, labels = load_data(args.data_path)

    # Train the model
    model.fit(features, labels, epochs=1, batch_size=32)

    # Save the weights
    model.save_weights(weights_file)

if args.validate:
    # Evaluate the model
    client = Client("http://localhost:8080")
    
    # To simulate, simply pass the name of the file in the precomputed folder     
    response : Response = get_validate_model.sync_detailed(client=client, model=GetValidateModelModel.CIFAR10, weights=weights_file)
    
    if isinstance(response.parsed, GetValidateModelResponse200):
        if isinstance(response.parsed.error, Unset):
            print("Model validation successful")
        else:
            print("Model validation failed")
    else:
        print("Error:", response.status_code)