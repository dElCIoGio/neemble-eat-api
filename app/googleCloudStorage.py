import os
from google.cloud import storage


if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") is None:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials/credentials.json"

storage_client = storage.Client()
bucketName = "neemble-eat-image-storage"


def uploadFile(file_path, filename, folder_path, bucket_name=bucketName):
    try:
        # Initialize the Google Cloud Storage client and get the bucket
        bucket = storage_client.get_bucket(bucket_name)

        # Create the full path for the file in the bucket
        full_path = f"{folder_path}/{filename}" if folder_path else filename

        # Create a blob object and upload the file from the local path
        blob = bucket.blob(full_path)
        blob.upload_from_filename(file_path)

        # Return the public URL for the uploaded file
        return blob.public_url
    except Exception as error:
        print(error)
        return None

def deleteFile(filename, folder_path, bucket_name=bucketName):
    try:
        # Get the bucket from the storage client
        bucket = storage_client.get_bucket(bucket_name)

        # Create the full path for the file in the bucket
        full_path = f"{folder_path}/{filename}" if folder_path else filename

        # Get the blob object for the given file path
        blob = bucket.blob(full_path)

        # Delete the blob
        blob.delete()

        # Return a message confirming deletion
        return f"File '{full_path}' deleted from bucket '{bucket_name}'."
    except Exception as error:
        print(error)
        return None