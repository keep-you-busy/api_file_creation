import pickle
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload


class GoogleDriveService:
    def __init__(self, client_secret_file, api_name, api_version, scopes):
        self.client_secret_file = client_secret_file
        self.api_name = api_name
        self.api_version = api_version
        self.scopes = scopes
        self.credentials = self._get_credentials()

    def _get_credentials(self):
        pickle_file = f'token_{self.api_name}_{self.api_version}.pickle'

        if os.path.exists(pickle_file):
            with open(pickle_file, 'rb') as token:
                credentials = pickle.load(token)

            if credentials and credentials.valid:
                return credentials

        return self._create_credentials(pickle_file)

    def _create_credentials(self, pickle_file):
        flow = InstalledAppFlow.from_client_secrets_file(
            self.client_secret_file, self.scopes)
        credentials = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(credentials, token)

        return credentials

    def create_drive_file(self, data, name):
        file_metadata = {'name': name}
        media = MediaInMemoryUpload(
            data.encode('utf-8'), mimetype='text/plain', resumable=True)

        try:
            drive_service = build(
                self.api_name, self.api_version, credentials=self.credentials)
            drive_service.files().create(
                body=file_metadata, media_body=media).execute()
            return {'status': 'success'}
        except Exception as error:
            raise Exception(f'Error raised: {error}')
