from methods.gcs_handler import GCSHandler
from methods.sensible import SensibleExtractor


class ExtractionRouter:
    def __init__(self, data):
        self.data = data
        self.bucket_name = data["bucket_name"]
        self.file_path = data["file_path"]
        self.configuration = data["configuration"]

        # Instantiate GCSHandler
        self.gcs_handler = GCSHandler(
            bucket_name=self.bucket_name, file_path=self.file_path
        )
        self.sensible_secret = self.sensible_secret = self.gcs_handler.get_secret(
            secret_name="SENSIBLE_KEY"
        )
        # Generate signed_url for document
        self.signed_url = self.gcs_handler.generate_signed_url()

    def route_extraction(self):
        extractor = SensibleExtractor(self.data, self.sensible_secret)
        webhook_url = self.configuration["webhook_url"]
        extraction_response = extractor.post_extraction(self.signed_url, webhook_url)
        return extraction_response
