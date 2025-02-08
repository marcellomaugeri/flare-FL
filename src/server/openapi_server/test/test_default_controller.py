import unittest

from flask import json

from openapi_server.models.validate_model_post200_response import ValidateModelPost200Response  # noqa: E501
from openapi_server.models.validate_model_post_request import ValidateModelPostRequest  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_validate_model_post(self):
        """Test case for validate_model_post

        Validate the model with provided weights
        """
        validate_model_post_request = openapi_server.ValidateModelPostRequest()
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/validate_model',
            method='POST',
            headers=headers,
            data=json.dumps(validate_model_post_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
