import argparse
from models.cifar10 import get_model
import numpy as np
from utils.cifar10_utils import load_data
from model_update_and_validation_api_client import Client
from model_update_and_validation_api_client.models import PostUpdateModelBody, PostUpdateModelBodyModelId, PostUpdateModelFromFileBody, PostUpdateModelFromFileBodyModelId, PostUpdateModelFromFileResponse200, PostUpdateModelFromFileResponse400, PostUpdateModelResponse200, PostUpdateModelResponse400, GetGlobalModelResponse400, GetGlobalModelResponse404, GetValidateResponse200, GetValidateResponse400, GetValidateResponse409, post_update_model_body
from model_update_and_validation_api_client.api.default import get_get_local_update, get_global_model, get_validate, post_update_model, post_update_model_from_file
from model_update_and_validation_api_client.types import Response, Unset
import os

parser = argparse.ArgumentParser(description='Train a model.')
parser.add_argument('--data-path', type=str, default='data/cifar10/data_batch_1', help='Path to the training data')
parser.add_argument('--validate', action='store_true', help='Validate the model after training')
parser.add_argument('--train', action='store_true', help='Enable training (disabled because of the precomputed weights)')
parser.add_argument('--upload', action='store_true', help='Perform a local update')
parser.add_argument('--get', action='store_true', help='Get the local update')
parser.add_argument('--get-global', action='store_true', help='Get the global model')

args = parser.parse_args()

if not args.train and not args.validate and not args.upload and not args.get and not args.get_global:
    print("Please specify an action: --train, --validate, --upload, --get")

index = args.data_path[-1]
weights_file = f'data/cifar10/precomputed/precomputed_{index}.weights.h5'

if args.get: # get the local update specified by the model_id and the update_id
    model_id = "cifar10"
    update_id = "412e758abe56e0fe6d33dad4490b7c30a80db120297a0cbd6082c592d0e90632"
    
    _model = get_model()
    
    client = Client("http://localhost:8080")
    
    response : Response = get_get_local_update.sync_detailed(client=client, model_id=model_id, update_id=update_id)
    
    if isinstance(response.parsed, GetGlobalModelResponse404):
        print("Model not found")
    elif isinstance(response.parsed, GetGlobalModelResponse400):
        print("Error:", response.parsed)
    elif isinstance(response.parsed, str):
        _model.load_weights(response.parsed)
        #if we arrive here, the model has been loaded successfully
        
if args.get_global:
    model_id = "cifar10"
    
    _model = get_model()
    
    client = Client("http://localhost:8080")
    
    response : Response = get_global_model.sync_detailed(client=client, model_id=model_id)
    
    if isinstance(response.parsed, GetGlobalModelResponse404):
        print("Model not found")
    elif isinstance(response.parsed, GetGlobalModelResponse400):
        print("Error:", response.parsed)
    elif isinstance(response.parsed, str):
        _model.load_weights(response.parsed)
        #if we arrive here, the model has been loaded successfully

if args.train:
    model = get_model()

    # Load the CIFAR-10 dataset
    features, labels = load_data(args.data_path)

    # Train the model
    model.fit(features, labels, epochs=1, batch_size=32)

    # Save the weights
    model.save_weights(weights_file)
    
if args.upload:
    # Upload the weights
    client = Client("http://localhost:8080")
    
    with open(weights_file, 'rb') as f:
        weights64 = f.read().hex()
        
    model_id = PostUpdateModelFromFileBodyModelId.CIFAR10
    
    request_body : PostUpdateModelBody = PostUpdateModelBody(model_id=model_id, hex_weights=weights64)
    
    response : Response = post_update_model.sync_detailed(client=client, body=request_body)
    
    if not isinstance(response.parsed, PostUpdateModelResponse200):
        print("Error:", response.status_code)
    else:
        print("Update ID:", response.parsed)

if args.validate:
    # Evaluate the model
    client = Client("http://localhost:8080")
    
    model_id = PostUpdateModelFromFileBodyModelId.CIFAR10
    
    response : Response = get_validate.sync_detailed(client=client, model_id=model_id, update_id="412e758abe56e0fe6d33dad4490b7c30a80db120297a0cbd6082c592d0e90632")
    
    if isinstance(response.parsed, GetValidateResponse200):
        print("model_id:", response.parsed.model_id, "update_id:", response.parsed.update_id)
    else:
        print("Error:", response.status_code) 