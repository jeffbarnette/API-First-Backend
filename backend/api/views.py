from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

from .serializers import FileSerializer
from .models import File
from config.settings import MEDIA_ROOT


class GetFileView(APIView):
    """Main class to retrieve file information"""
    def get(self, request, upload_id):
        """Handles retrieving of uploaded file information"""
        try:
            upload_id = int(upload_id) # Ensure id is integer
            file = File.objects.get(pk=upload_id)
        except (ValueError, File.DoesNotExist):
            return Response('Invalid upload id provided!', 
                status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = FileSerializer(file)
            file_details = {
                "upload_id": serializer.data['id'],
                "num_of_rows": serializer.data['rows'],
                "items": serializer.data['items']
            }
            return Response(file_details, status=status.HTTP_200_OK)


class PostFileView(APIView):
    """Main class to handle file uploads"""
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format='txt'):
        """Handles uploading and processing of file."""
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            # Save first to upload the file
            file_serializer.save()
            # Parse the uploaded file
            up_file = request.FILES['file']
            count = 0
            items = []
            try:
                with open(f'{MEDIA_ROOT}/files/{up_file.name}', 'r') as file:
                    lines = file.readlines()
                    for line in lines:
                        count += 1
                        row_items = line.rstrip('\n').split('|')
                        items.append(row_items[1].strip())
            except FileNotFoundError:
                return Response('Unable to locate file to parse!', 
                    status=status.HTTP_404_NOT_FOUND)
            else:
                # Save the parsed data
                items = ', '.join(items) # Make list a string
                file_obj = file_serializer.save(rows=count, items=items)
                response_json = {
                    "upload_id": file_obj.id
                }
                return Response(response_json, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST)