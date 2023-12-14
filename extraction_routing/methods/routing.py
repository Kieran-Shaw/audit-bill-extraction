from methods.gcs_handler import GCSHandler
from methods.google_ai import GoogleDocumentAIExtractor
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

        # Get sensible secret only if config method is sensible
        self.sensible_secret = None
        if self.configuration["method"] == "sensible":
            self.sensible_secret = self.gcs_handler.get_secret(
                secret_name="SENSIBLE_KEY"
            )

        # Get presigned URL only if method is sensible
        self.signed_url = None
        if self.configuration["method"] == "sensible":
            self.signed_url = self.gcs_handler.generate_signed_url()

    def route_extraction(self):
        # if sensible
        if self.configuration["method"] == "sensible":
            extractor = SensibleExtractor(self.data, self.sensible_secret)
            webhook_url = self.configuration[
                "webhook_url"
            ]  # cloud function sensible post process url
            webhook_payload = self.data  # Replace with your custom payload
            extraction_response = extractor.post_extraction(
                self.signed_url, webhook_url, webhook_payload
            )
            return extraction_response

        # if google document ai
        elif self.configuration["method"] == "google_document_ai":
            extractor = GoogleDocumentAIExtractor(self.configuration)
            # Perform Google Document AI extraction
            # ...
        else:
            raise ValueError("Unsupported extraction method")
