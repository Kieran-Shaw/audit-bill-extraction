from storage_operations import create_folder_in_bucket


def create_folder(request):
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and "bucket_name" in request_json and "folder_name" in request_json:
        bucket_name = request_json["bucket_name"]
        folder_name = request_json["folder_name"]
    elif (
        request_args and "bucket_name" in request_args and "folder_name" in request_args
    ):
        bucket_name = request_args["bucket_name"]
        folder_name = request_args["folder_name"]
    else:
        return "Error: Please specify both bucket_name and folder_name."

    return create_folder_in_bucket(bucket_name, folder_name)
