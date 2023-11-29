from google.cloud import storage


def create_folder_in_bucket(bucket_name, folder_name):
    """Create a folder in a Google Cloud Storage bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # The folder is created by uploading an empty blob with the folder name ending with "/"
    blob = bucket.blob(folder_name + "/")
    blob.upload_from_string("")

    return f"Folder {folder_name}/ created in bucket {bucket_name}."
