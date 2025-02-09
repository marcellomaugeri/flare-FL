import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.global_model_get404_response import GlobalModelGet404Response  # noqa: E501
from openapi_server.models.update_model_from_file_post200_response import UpdateModelFromFilePost200Response  # noqa: E501
from openapi_server.models.update_model_from_file_post_request import UpdateModelFromFilePostRequest  # noqa: E501
from openapi_server.models.update_model_post200_response import UpdateModelPost200Response  # noqa: E501
from openapi_server.models.update_model_post400_response import UpdateModelPost400Response  # noqa: E501
from openapi_server.models.update_model_post_request import UpdateModelPostRequest  # noqa: E501
from openapi_server.models.validate_get200_response import ValidateGet200Response  # noqa: E501
from openapi_server.models.validate_get400_response import ValidateGet400Response  # noqa: E501
from openapi_server.models.validate_get409_response import ValidateGet409Response  # noqa: E501
from openapi_server import util

from openapi_server.mlmodels import get_model
from base64 import b64encode
from openapi_server.utils.cifar10_utils import load_data
from eth_utils import encode_hex
import hashlib

def construct_file_name(model_id, update_id) -> str:
    return f"{model_id}_{update_id}.weights.h5"

def split_file_name(file_name) -> Tuple[str, str]:
    return file_name.split("_")

def construct_file_path(file_name) -> str:
    return f"../data/{file_name}"


def get_local_update_get(model_id, update_id):  # noqa: E501
    """Get local update weights.

     # noqa: E501

    :param model_id: 
    :type model_id: str
    :param update_id: 
    :type update_id: str

    :rtype: Union[str, Tuple[str, int], Tuple[str, int, Dict[str, str]]
    """
    file_path = construct_file_path(construct_file_name(model_id, update_id))
    
    with open(file_path, 'rb') as f:
        weights64 = encode_hex(f.read())
        return weights64
    
def global_model_get(model_id):  # noqa: E501
    """Retrieve global model weights.

     # noqa: E501

    :param model_id: 
    :type model_id: str

    :rtype: Union[str, Tuple[str, int], Tuple[str, int, Dict[str, str]]
    """
    # we use the prebuilt #5 as global model
    file_path = construct_file_path("cifar10/precomputed/precomputed_5.weights.h5")
    
    with open(file_path, 'rb') as f:
        weights64 = encode_hex(f.read())
        return weights64


# Unused for now
def update_model_from_file_post(body):  # noqa: E501
    """Update model from file.

     # noqa: E501

    :param update_model_from_file_post_request: 
    :type update_model_from_file_post_request: dict | bytes

    :rtype: Union[UpdateModelFromFilePost200Response, Tuple[UpdateModelFromFilePost200Response, int], Tuple[UpdateModelFromFilePost200Response, int, Dict[str, str]]
    """
    update_model_from_file_post_request = body
    if connexion.request.is_json:
        update_model_from_file_post_request = UpdateModelFromFilePostRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def update_model_post(body):  # noqa: E501
    """Update model with hex string containing weights.

     # noqa: E501

    :param update_model_post_request: 
    :type update_model_post_request: dict | bytes

    :rtype: Union[UpdateModelPost200Response, Tuple[UpdateModelPost200Response, int], Tuple[UpdateModelPost200Response, int, Dict[str, str]]
    """
    update_model_post_request = body
    if connexion.request.is_json:
        update_model_post_request = UpdateModelPostRequest.from_dict(connexion.request.get_json())  # noqa: E501
        
    _model = get_model(update_model_post_request.model_id)
    
    _weights_hex = update_model_post_request.hex_weights
    
    # Decode the hex string to bytes
    _weights_bytes = bytes.fromhex(_weights_hex)
        
    _digest = hashlib.sha256(_weights_bytes).hexdigest()

    # Save the weights in a file
    file_name = construct_file_name(update_model_post_request.model_id, _digest)
    file_path = construct_file_path(file_name)
    with open(file_path, 'wb') as f:
        f.write(_weights_bytes)
    
    return UpdateModelPost200Response(update_id=_digest)
    
def validate_get(model_id, update_id):  # noqa: E501
    """Validate model update.

     # noqa: E501

    :param model_id: 
    :type model_id: str
    :param update_id: 
    :type update_id: str

    :rtype: Union[ValidateGet200Response, Tuple[ValidateGet200Response, int], Tuple[ValidateGet200Response, int, Dict[str, str]]
    """
    # Load the model
    _model = get_model(model_id)
    _global_model = get_model(model_id)
    
    # Load the update
    file_path = construct_file_path(construct_file_name(model_id, update_id))   
    global_file_path = construct_file_path("cifar10/precomputed/precomputed_5.weights.h5") 
    # Load the weights
    _model.load_weights(file_path)
    _global_model.load_weights(global_file_path)
    
    # Load the CIFAR-10 dataset
    features, labels = load_data("../data/cifar10/test_batch")
    
    # Test the model and get metrics
    loss, accuracy = _model.evaluate(features, labels)
    
    
    # Test the global model and get metrics
    loss_global, accuracy_global = _global_model.evaluate(features, labels)
    
    # Compare the metrics
    if accuracy > accuracy_global:
        return ValidateGet200Response(model_id=model_id, update_id=update_id)
    else:
        return ValidateGet409Response(error="Not valid")
