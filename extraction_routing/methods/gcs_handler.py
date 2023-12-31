import datetime
import json
import os

from google.cloud import secretmanager, storage
from google.oauth2 import service_account


class GCSHandler:
    def __init__(
        self,
        bucket_name: str,
        file_path: str,
        project_id: str = "small-group-quote",
    ):
        # Initialize GCS client
        self.storage_client = storage.Client()
        self.bucket_name = bucket_name
        self.source_blob_name = file_path

        ## Initialize Secret client
        self.secret_client = secretmanager.SecretManagerServiceClient()

    def get_secret(self, secret_name: str):
        name = f"projects/small-group-quote/secrets/{secret_name}/versions/latest"
        response = self.secret_client.access_secret_version(name=name)
        return response.payload.data.decode("UTF-8")

    def generate_signed_url(self):
        """Read a file from Google Cloud Storage."""
        bucket = self.storage_client.bucket(self.bucket_name)
        blob = bucket.blob(self.source_blob_name)
        signed_url = blob.generate_signed_url(
            version="v4",
            # This URL is valid for specified minutes
            expiration=datetime.timedelta(minutes=5),
            # Allow GET requests using this URL.
            method="GET",
            credentials=self.get_credentials(),
        )
        return signed_url

    def get_credentials(self):
        """Returns a Google service account credentials object."""
        service_account_json_str = self.get_secret("SERVICE_ACCOUNT_CREDS")
        service_account_info = json.loads(service_account_json_str)
        credentials = service_account.Credentials.from_service_account_info(
            service_account_info
        )
        return credentials
