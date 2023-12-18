import pandas as pd
from google.cloud import documentai, storage


class RequestDocAI:
    def __init__(self, request_json):
        self.request_json = request_json
        self.bucket_name = self.request_json["bucket_name"]
        self.file_path = self.request_json["file_path"]
        self.processor_id = self.request_json["configuration"]["processor_id"]

    def get_file(self):
        """Gets the file from the bucket_name and file_path."""

        # Create a client
        storage_client = storage.Client()

        # Get the bucket
        bucket = storage_client.bucket(self.bucket_name)

        # Get the file
        file = bucket.blob(self.file_path)

        # Download the file bytes
        file_bytes = file.download_as_bytes()

        # Return the file bytes
        return file_bytes

    def process_document(self):
        """Processes the document using the Document AI processor."""

        # Create a client
        document_ai_client = documentai.DocumentProcessorServiceClient()

        # Get the full path of the processor
        processor_path = document_ai_client.processor_path(
            project="small-group-quote",
            location="us",
            processor=self.processor_id,
        )

        # Read the file bytes
        file_bytes = self.get_file()

        # Load the file bytes into a RawDocument object
        raw_document = documentai.RawDocument(
            content=file_bytes, mime_type="application/pdf"
        )

        # Configure the process request
        request = documentai.ProcessRequest(
            name=processor_path, raw_document=raw_document
        )

        # Make the process request
        result = document_ai_client.process_document(request=request)

        # Get the document, convert the response to json, get entities
        document = documentai.Document.to_dict(result.document)
        document_json = documentai.Document.to_json(result.document)
        with open("document.json", "w") as f:
            f.write(document_json)

        document_entities = document["entities"]

        # Check if there are any entities
        if not document_entities:
            raise Exception("No entities found in document")

        # Return the document entities
        return document_entities
