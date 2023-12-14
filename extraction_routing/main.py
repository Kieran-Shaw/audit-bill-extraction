import flask

# import functions_framework
from methods.routing import ExtractionRouter


# @functions_framework.http
def extraction_routing(request: flask.Request):
    """Cloud function to extract metadata from a file using the Sensible API."""
    try:
        request_json = request.get_json()

        # Validate required parameters
        required_params = ["bucket_name", "file_path", "configuration"]
        if not all(param in request_json for param in required_params):
            missing_params = [
                param for param in required_params if param not in request_json
            ]
            return f"Missing required parameters: {', '.join(missing_params)}", 400

        # Instantiate ExtractionRouter with the request data
        router = ExtractionRouter(data=request_json)

        # Route the extraction process
        extraction_result = router.route_extraction()

        return flask.jsonify(extraction_result)

    except Exception as e:
        print(e)
        return f"An error occurred: {str(e)}", 500
