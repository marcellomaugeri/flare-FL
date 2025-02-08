import unittest

from flask import json

from openapi_server.models.validate_model_get200_response import ValidateModelGet200Response  # noqa: E501
from openapi_server.models.validate_model_get_request import ValidateModelGetRequest  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_validate_model_get(self):
        """Test case for validate_model_get

        Validate the model with provided weights
        """
        validate_model_get_request = openapi_server.ValidateModelGetRequest()
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/validate_model',
            method='GET',
            headers=headers,
            data=json.dumps(validate_model_get_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
