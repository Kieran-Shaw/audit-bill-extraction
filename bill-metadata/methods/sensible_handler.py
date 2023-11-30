import base64
import os

import requests
from dotenv import load_dotenv


class SensibleAPIHandler:
    def __init__(self, config_name: str, environment: str):
        load_dotenv()
        self.sensible_key = os.getenv("SENSIBLE_KEY")
        self.document_type = "bill_metadata"
        self.config_name = config_name
        self.environment = environment
        self.api_url = f"https://api.sensible.so/v0/extract/{self.document_type}/{self.config_name}?environment={self.environment}"

    @staticmethod
    def encode_file(file_bytes):
        """Encode the file content to base64."""
        return base64.b64encode(file_bytes).decode("utf-8")

    def make_api_request(self, encoded_document, document_name):
        """Make an API request with the encoded document."""
        payload = {"document": encoded_document}
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.sensible_key}",
            "document_name": document_name,
        }

        return requests.post(self.api_url, json=payload, headers=headers)
