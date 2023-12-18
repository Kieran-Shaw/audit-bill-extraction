import sys

import flask
import functions_framework
from methods.normalize_response import NormalizeResponse
from methods.request_doc_ai import RequestDocAI


@functions_framework.http
def request_doc_ai(request: flask.Request):
    """Cloud function to extract metadata from a file using the Sensible API."""
    try:
        request_json = request.get_json()

        # Validate required parameters
        required_params = ["id", "bucket_name", "file_path", "configuration"]
        if not all(param in request_json for param in required_params):
            missing_params = [
                param for param in required_params if param not in request_json
            ]
            return f"Missing required parameters: {', '.join(missing_params)}", 400

        # Instantiate the RequestDocAI class
        doc_ai_client = RequestDocAI(request_json=request_json)

        # Get the extraction
        document_entities = doc_ai_client.process_document()

        # Instantiate the NormalizeResponse class
        normalizer = NormalizeResponse(document_entities=document_entities)
        standard_df = normalizer.get_normal_entities_df()
        line_items_df = normalizer.get_line_items_df()

        # Save to csv file
        standard_df.to_csv("standard_df.csv", index=False)
        line_items_df.to_csv("line_items_df.csv", index=False)

        # Return the response
        return "hi"

    except Exception as e:
        print(sys.exc_info().__dict__)
        return f"An error occurred: {str(e)}", 500
