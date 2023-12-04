import flask
from methods.gcs_handler import GCSHandler
from methods.gpt_handler import GPTHandler


def extract_line_items(request: flask.Request):
    """Cloud function to extract metadata from a file using the Sensible API."""
    try:
        request_json = request.get_json()

        # Validate required parameters
        required_params = [
            "bucket_name",
            "file_name",
            "carrier",
            "prompt",
            "environment",
        ]
        if not all(param in request_json for param in required_params):
            missing_params = [
                param for param in required_params if param not in request_json
            ]
            return f"Missing required parameters: {', '.join(missing_params)}", 400

        bucket_name = request_json["bucket_name"]
        file_name = request_json["file_name"]
        carrier = request_json["carrier"]
        prompt = request_json["prompt"]
        environment = request_json["environment"]

        # Instantiate GCS Handler and get openai secret
        gcs_handler = GCSHandler(
            bucket_name=bucket_name,
            dataset_name="extractions",
            table_name="bill_metadata_extractions",
        )
        openai_secret = gcs_handler.get_secret(secret_name="OPENAI_API_KEY")
        gpt_handler = GPTHandler(openai_key=openai_secret, prompt=prompt)

        # Read the file from Google Cloud Storage
        file_bytes = gcs_handler.read_file(source_blob_name=file_name)

        # Upload file to OpenAI, start Assitant

    except Exception as e:
        print(e)
        return f"An error occurred: {str(e)}", 500
