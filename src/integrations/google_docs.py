from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from config.settings import settings


class GoogleDocs:
    def __init__(self):
        self.credentials_file = settings.GOOGLE_SERVICE_ACCOUNT
        self.folder_id = settings.GOOGLE_DRIVE_FOLDER_ID
        self.scopes = settings.GOOGLE_SCOPES
        self.email = settings.GOOGLE_EMAIL

    def create_google_doc(self, title, content):
        credentials = service_account.Credentials.from_service_account_file(
            self.credentials_file, scopes=self.scopes)

        docs_service = build('docs', 'v1', credentials=credentials)
        drive_service = build('drive', 'v3', credentials=credentials)

        doc_body = {
            'title': title
        }

        document = docs_service.documents().create(body=doc_body).execute()
        document_id = document.get('documentId')

        requests = [
            {
                'insertText': {
                    'location': {
                        'index': 1
                    },
                    'text': content
                }
            }
        ]

        docs_service.documents().batchUpdate(
            documentId=document_id,
            body={'requests': requests}
        ).execute()

        if self.folder_id:
            try:
                file = drive_service.files().get(
                    fileId=document_id,
                    fields='parents'
                ).execute()

                previous_parents = ",".join(file.get('parents', []))

                drive_service.files().update(
                    fileId=document_id,
                    addParents=self.folder_id,
                    removeParents=previous_parents,
                    fields='id, parents'
                ).execute()
            except HttpError as error:
                print(f"Error moving document to folder: {error}")

        if self.email:
            try:
                user_permission = {
                    'type': 'user',
                    'role': 'writer',
                    'emailAddress': self.email
                }

                drive_service.permissions().create(
                    fileId=document_id,
                    body=user_permission,
                    sendNotificationEmail=True
                ).execute()
            except HttpError as error:
                print(f"Error sharing document: {error}")

        doc_url = f"https://docs.google.com/document/d/{document_id}/edit"

        return document_id, doc_url
