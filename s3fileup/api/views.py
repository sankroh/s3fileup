"""
DRF API view to get a temporary Amazon S3 url to upload files to
"""

from rest_framework.decorators import api_view
from rest_framework.exceptions import ParseError
from rest_framework.response import Response

from s3fileup.utils import generate_signed_url

@api_view(['POST'])
def generate_s3_url(request):
    """
    Generates a one time use URL for uploading files to S3
    """
    s3_object_type = request.POST.get('s3_object_type', 'application/octet-stream')
    s3_object_name = request.POST.get('s3_object_name', None)

    if not s3_object_name:
        raise ParseError('You need to provide object name and type')

    url = generate_signed_url(s3_object_name, s3_object_type, method='PUT')

    result = { 'upload_url' : url }
    return Response(result)

