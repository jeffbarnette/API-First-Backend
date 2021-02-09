from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from ..models import File

class FileModelTests(TestCase):
    def test_file_string_representation(self):
        """Test File string representation"""
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
        
        new_file = File.objects.create(
            file=test_file,
            rows=5,
            items='Eggs, Bread, Butter, Milk, Corn'
        )

        first_file = File.objects.first()
        self.assertEqual(str(first_file), new_file.file.name)
    
    def test_file_has_details(self):
        """Test File has details from file"""
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
        
        new_file = File.objects.create(
            file=test_file,
            rows=5,
            items='Eggs, Bread, Butter, Milk, Corn'
        )

        file_details = File.objects.get(id=new_file.id)
        self.assertEqual(file_details.file.name, new_file.file.name)
        self.assertEqual(file_details.rows, new_file.rows)
        self.assertEqual(file_details.items, new_file.items)

