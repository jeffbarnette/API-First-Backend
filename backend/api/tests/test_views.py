from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, RequestFactory

from ..models import File
from ..views import GetFileView, PostFileView

class APIViewTests(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_get_details(self):
        """Test retrieving file details"""
        # Create a sample file
        test_file = SimpleUploadedFile(
            "sample.txt", bytes('123', encoding='UTF-8'),
            content_type="text/txt"
        )
        # Create sample file record
        new_file = File.objects.create(
            file=test_file,
            rows=5,
            items='Eggs, Bread, Butter, Milk, Corn'
        )

        # Create an instance of a GET request.
        request = self.factory.get('/api/upload/')

        # Test GetFileView() as if it were deployed at /api/upload
        response = GetFileView.as_view()(request, upload_id=new_file.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data,
            {
                'upload_id': new_file.id,
                'num_of_rows': new_file.rows,
                'items': new_file.items
            }
        )
    
    def test_post_new_file(self):
        """Test posting a new file"""
        # Create sample file
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

        # Create an instance of a POST request.
        request = self.factory.post('/api/upload/', data)

        # Test PostFileView() as if it were deployed at /api/upload
        response = PostFileView.as_view()(request)
        self.assertEqual(response.status_code, 201)
        self.assertIn('upload_id',response.data)