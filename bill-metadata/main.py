import flask

# import functions_framework
from methods.gcs_handler import GCSHandler
from methods.sensible_handler import SensibleAPIHandler
from methods.sensible_response_handler import SensibleResponseHandler


# @functions_framework.http
def extract_metadata(request: flask.Request):
    """Cloud function to extract metadata from a file using the Sensible API."""
    try:
        request_json = request.get_json()

        # Validate required parameters
        required_params = ["bucket_name", "file_name", "carrier", "environment"]
        if not all(param in request_json for param in required_params):
            missing_params = [
                param for param in required_params if param not in request_json
            ]
            return f"Missing required parameters: {', '.join(missing_params)}", 400

        bucket_name = request_json["bucket_name"]
        file_name = request_json["file_name"]
        carrier = request_json["carrier"]
        environment = request_json["environment"]

        gcs_handler = GCSHandler(
            bucket_name=bucket_name,
            dataset_name="extractions",
            table_name="bill_metadata_extractions",
        )
        # Get the secret from Google Secret Manager
        sensible_secret = gcs_handler.get_secret(secret_name="SENSIBLE_KEY")

        sensible_handler = SensibleAPIHandler(
            sensible_key=sensible_secret, config_name=carrier, environment=environment
        )

        # Read the file from Google Cloud Storage
        file_bytes = gcs_handler.read_file(source_blob_name=file_name)

        # Encode the file to base64
        encoded_document = sensible_handler.encode_file(file_bytes=file_bytes)

        # Make the API request to Sensible API
        response = sensible_handler.make_api_request(
            encoded_document=encoded_document, document_name=file_name
        )

        # Save the response to BigQuery table
        bigquery_uuid = gcs_handler.save_to_bigquery(
            carrier_name=carrier, response_json=response.json()
        )

        # Instantiate the sensible response handler
        sensible_response_handler = SensibleResponseHandler(
            json_response=response.json(), carrier=carrier, bigquery_uuid=bigquery_uuid
        )

        parsed_response = sensible_response_handler.process_response()

        return parsed_response

    except Exception as e:
        print(e)
        return f"An error occurred: {str(e)}", 500
