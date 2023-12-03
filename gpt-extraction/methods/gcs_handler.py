import datetime
import json
import uuid

from google.cloud import bigquery, secretmanager, storage


class GCSHandler:
    def __init__(
        self,
        bucket_name: str,
        dataset_name: str,
        table_name: str,
        project_id: str = "small-group-quote",
    ):
        # Initialize GCS client
        self.storage_client = storage.Client(project=project_id)
        self.bucket_name = bucket_name
        self.source_blob_name = None

        ## Initialize Secret client
        self.secret_client = secretmanager.SecretManagerServiceClient()

        # Initialize BigQuery client and set dataset and table
        self.bigquery_client = bigquery.Client(project=project_id)
        self.dataset_name = dataset_name
        self.table_name = table_name

    def get_secret(self, secret_name: str):
        name = f"projects/small-group-quote/secrets/{secret_name}/versions/latest"
        response = self.secret_client.access_secret_version(name=name)
        return response.payload.data.decode("UTF-8")

    def read_file(self, source_blob_name: str):
        """Read a file from Google Cloud Storage."""
        self.source_blob_name = source_blob_name
        bucket = self.storage_client.bucket(self.bucket_name)
        blob = bucket.blob(source_blob_name)
        return blob.download_as_bytes()

    def save_to_bigquery(self, carrier_name: str, response_json: dict):
        """Save data to a BigQuery table."""
        created_uuid = str(uuid.uuid4())
        table_id = f"{self.dataset_name}.{self.table_name}"

        json_string = json.dumps(response_json)

        rows_to_insert = [
            {
                "id": created_uuid,
                "carrier_name": carrier_name,
                "bucket_name": self.bucket_name,
                "file_path": self.source_blob_name,
                "sensible_extraction": json_string,
                "created_at": datetime.datetime.utcnow().isoformat(),
            }
        ]

        errors = self.bigquery_client.insert_rows_json(table_id, rows_to_insert)
        if errors != []:
            raise Exception(f"BigQuery insertion failed: {errors}")
        return created_uuid
