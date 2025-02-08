import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.validate_model_get200_response import ValidateModelGet200Response  # noqa: E501
from openapi_server import util

from openapi_server.mlmodels import get_model
from base64 import b64encode
from openapi_server.utils.cifar10_utils import load_data
from eth_utils import encode_hex


def validate_model_get(model, weights):  # noqa: E501
    """Validate the model with provided weights

     # noqa: E501

    :param model: The model architecture
    :type model: str
    :param weights: The model weights (to overcome the limitation of GET request, this field will receive a file path for now)
    :type weights: str

    :rtype: Union[ValidateModelGet200Response, Tuple[ValidateModelGet200Response, int], Tuple[ValidateModelGet200Response, int, Dict[str, str]]
    """
    _model = get_model(model)
    
    # prepend ../ to weights
    _model.load_weights("../"+weights) #Weights is a file path
    
    # Read the weights from the file as a base64 string
    with open("../"+weights, 'rb') as f:
        weights64 = encode_hex(f.read())
        #weights64 = "0x" + weights64.decode('utf-8')

            
    # Load the test data
    test_features, test_labels = load_data('../data/cifar10/test_batch')
    
    # Evaluate the model
    loss, accuracy = _model.evaluate(test_features, test_labels)
    
    
    
    if accuracy > 0.1:
        return ValidateModelGet200Response(model=model, weights=weights64, error=None)
    else:
        return ValidateModelGet200Response(model=model, weights=weights64, error='Model accuracy is too low')


