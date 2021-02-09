from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..models import File

api_client = APIClient()


class APITests(TestCase):
    def test_api_is_valid_endpoint(self):
        """Test a user can successfully query the API Redoc endpoint."""
        response = api_client.get(reverse("schema-redoc"))
        assert response.status_code == status.HTTP_200_OK
    
    def test_swagger_is_valid_endpoint(self):
        """Test a user can successfully query the API Swagger endpoint."""
        response = api_client.get(reverse("schema-swagger-ui"))
        assert response.status_code == status.HTTP_200_OK
    
    def test_upload_get_is_valid_endpoint(self):
        """Test a user can successfully query the GET upload endpoint."""
        response = api_client.get(
            reverse("get-upload",
            args=['1'])
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_upload_post_is_valid_endpoint(self):
        """Test a user can successfully query the POST endpoint."""
        response = api_client.post(
            reverse("post-upload")
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_upload_put_is_not_valid_method(self):
        """
        Test that a user gets and error when trying to use PUT request
        to upload endpoint.
        """
        response = api_client.put(
            reverse("post-upload")
        )
        error_message = 'Method "PUT" not allowed.'
        response.data['detail'][0] == error_message
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
    def test_upload_delete_is_not_valid_method(self):
        """
        Test that a user gets and error when trying to use DELETE request
        to upload endpoint.
        """
        response = api_client.delete(
            reverse("post-upload")
        )
        error_message = 'Method "DELETE" not allowed.'
        response.data['detail'][0] == error_message
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
    def test_can_post_upload_to_endpoint(self):
        """Test a user can sucessfully POST a file to upload endpoint."""
        file_content = bytes(
            """
            1001 | Eggs | 12\n
            1002 | Bread | 1\n
            1003 | Butter | 1\n
            1004 | Milk | 1\n
            1005 | Corn | 2
            """, encoding='UTF-8'
        )

        test_file = SimpleUploadedFile(
            "sample.txt", file_content, content_type="text/txt")
        
        data = {'file': test_file}
        response = api_client.post(
            reverse("post-upload"), data, format='multipart'
        )
        assert response.status_code == status.HTTP_201_CREATED
    
    def test_can_get_upload_details_from_endpoint(self):
        """Test a user can sucessfully GET file details from endpoint."""
        file_content = bytes(
            """
            1001 | Eggs | 12\n
            1002 | Bread | 1\n
            1003 | Butter | 1\n
            1004 | Milk | 1\n
            1005 | Corn | 2
            """, encoding='UTF-8'
        )

        test_file = SimpleUploadedFile(
            "sample.txt", file_content, content_type="text/txt")
        
        new_file_object = File.objects.create(
            file=test_file,
            rows=5,
            items='Eggs, Bread, Butter, Milk, Corn'
        )

        response = api_client.get(reverse("get-upload", args=['1']))
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'upload_id': 1,
            'num_of_rows':  5,
            'items': 'Eggs, Bread, Butter, Milk, Corn'
        }
    
    def test_error_when_not_including_file_to_post_endpoint(self):
        """
        Test a user gets an error when no file is included POST request 
        to upload endpoint.
        """
        data = {'file': ''}
        response = api_client.post(
            reverse("post-upload"), data, format='multipart'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error_message = ('The submitted data was not a file. '
        'Check the encoding type on the form.')
        assert response.data['file'][0] == error_message
    
    def test_error_when_endpoint_sent_invalid_ids_(self):
        """
        Test a user gets an error when sending invalid ids
        using the GET request to upload endpoint.
        """
        file_content = bytes(
            """
            1001 | Eggs | 12\n
            1002 | Bread | 1\n
            1003 | Butter | 1\n
            1004 | Milk | 1\n
            1005 | Corn | 2
            """, encoding='UTF-8'
        )

        test_file = SimpleUploadedFile(
            "sample.txt", file_content, content_type="text/txt")
        
        new_file_object = File.objects.create(
            file=test_file,
            rows=5,
            items='Eggs, Bread, Butter, Milk, Corn'
        )

        response = api_client.get(
            reverse("get-upload",
            args=['5']) # Using invalid integer
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data == 'Invalid upload id provided!'

        response = api_client.get(
            reverse("get-upload",
            args=['abc']) # Using letters
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data == 'Invalid upload id provided!'

        response = api_client.get(
            reverse("get-upload",
            args=['!@$?%']) # Using symbols
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data == 'Invalid upload id provided!'