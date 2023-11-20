from rest_framework.response import Response

from rest_framework.decorators import api_view
from api.utils import GoogleDriveService


@api_view(('POST',))
def create_file(request):
    data = request.POST.get('data')
    name = request.POST.get('name')

    CLIENT_SECRET_FILE = 'credentials.json'
    SCOPES = ['https://www.googleapis.com/auth/drive']

    drive_service = GoogleDriveService(
        CLIENT_SECRET_FILE,
        'drive',
        'v3',
        SCOPES)

    result = drive_service.create_drive_file(data, name)

    return Response(result)
