import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.validate_model_post200_response import ValidateModelPost200Response  # noqa: E501
from openapi_server.models.validate_model_post_request import ValidateModelPostRequest  # noqa: E501
from openapi_server import util

from openapi_server.mlmodels import get_model
from base64 import b64decode
from openapi_server.utils.cifar10_utils import load_data

def validate_model_post(body):  # noqa: E501
    """Validate the model with provided weights

     # noqa: E501

    :param validate_model_post_request: 
    :type validate_model_post_request: dict | bytes

    :rtype: Union[ValidateModelPost200Response, Tuple[ValidateModelPost200Response, int], Tuple[ValidateModelPost200Response, int, Dict[str, str]]
    """
    validate_model_post_request = body
    if connexion.request.is_json:
        validate_model_post_request = ValidateModelPostRequest.from_dict(connexion.request.get_json())  # noqa: E501
    
    model = get_model(validate_model_post_request.model)
    weights = validate_model_post_request.weights
    
    # Decode the weights from base64
    weights = b64decode(weights)
    
    # Save on /tmp/weights.h5 file
    with open('/tmp/test.weights.h5', 'wb') as f:
        f.write(weights)
    
    model.load_weights('/tmp/test.weights.h5')
    
    # Load the test data
    test_features, test_labels = load_data('../data/cifar10/test_batch')
    
    # Evaluate the model
    loss, accuracy = model.evaluate(test_features, test_labels)
    
    if accuracy > 0.1:
        print("A posto mbare, menza parola")
        return ValidateModelPost200Response(model=validate_model_post_request.model, weights=validate_model_post_request.weights, error=None)
    else:
        return ValidateModelPost200Response(model=validate_model_post_request.model, weights=validate_model_post_request.weights, error='Model accuracy is too low')
