import unittest

from flask import json

from openapi_server.models.global_model_get404_response import GlobalModelGet404Response  # noqa: E501
from openapi_server.models.update_model_from_file_post200_response import UpdateModelFromFilePost200Response  # noqa: E501
from openapi_server.models.update_model_from_file_post_request import UpdateModelFromFilePostRequest  # noqa: E501
from openapi_server.models.update_model_post200_response import UpdateModelPost200Response  # noqa: E501
from openapi_server.models.update_model_post400_response import UpdateModelPost400Response  # noqa: E501
from openapi_server.models.update_model_post_request import UpdateModelPostRequest  # noqa: E501
from openapi_server.models.validate_get200_response import ValidateGet200Response  # noqa: E501
from openapi_server.models.validate_get400_response import ValidateGet400Response  # noqa: E501
from openapi_server.models.validate_get409_response import ValidateGet409Response  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_get_local_update_get(self):
        """Test case for get_local_update_get

        Get local update weights.
        """
        query_string = [('model_id', 'model_id_example'),
                        ('update_id', 'update_id_example')]
        headers = { 
            'Accept': 'application/octet-stream',
        }
        response = self.client.open(
            '/get_local_update',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_global_model_get(self):
        """Test case for global_model_get

        Retrieve global model weights.
        """
        query_string = [('model_id', 'model_id_example')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/global_model',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_model_from_file_post(self):
        """Test case for update_model_from_file_post

        Update model from file.
        """
        update_model_from_file_post_request = openapi_server.UpdateModelFromFilePostRequest()
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/update_model_from_file',
            method='POST',
            headers=headers,
            data=json.dumps(update_model_from_file_post_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_model_post(self):
        """Test case for update_model_post

        Update model with hex string.
        """
        update_model_post_request = openapi_server.UpdateModelPostRequest()
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/update_model',
            method='POST',
            headers=headers,
            data=json.dumps(update_model_post_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_validate_get(self):
        """Test case for validate_get

        Validate model update.
        """
        query_string = [('model_id', 'model_id_example'),
                        ('update_id', 'update_id_example')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/validate',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
