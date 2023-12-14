import datetime

from google.cloud import secretmanager, storage


class GCSHandler:
    def __init__(
        self,
        bucket_name: str,
        file_path: str,
        project_id: str = "small-group-quote",
    ):
        # Initialize GCS client
        self.storage_client = storage.Client(project=project_id)
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
            # This URL is valid for specified minutes
            expiration=datetime.timedelta(minutes=5),
            # Allow GET requests using this URL.
            method="GET",
        )
        return signed_url
