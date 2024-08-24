import os
import requests
from google.cloud import storage


if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") is None:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials/neemble-eat-db-c49af78976aa.json"

storage_client = storage.Client()
bucketName = "neemble-eat-image-storage"


def uploadFile(image_url, filename, folder_path, bucket_name=bucketName):
    """
    filename: the name you want the file to have in the storage bucket.
    folder_path: the local path to the file you want to upload.
    bucket_name: the name of the bucket where the file will be uploaded, though in your function this is already preset.
    """
    try:
        response = requests.get(image_url)
        response.raise_for_status()

        bucket = storage_client.get_bucket(bucket_name)

        full_path = f"{folder_path}/{filename}" if folder_path else filename

        blob = bucket.blob(full_path)
        blob.upload_from_string(response.content, content_type=response.headers["Content-Type"])

        return blob.public_url
    except Exception as error:
        print(error)
        return None

# result = uploadFile(image_url="https://v5.airtableusercontent.com/v3/u/32/32/1724191200000/VAWgrwcQpVc0DgLFv7KTDA/DSJ4kDXMkks0AjecRBG9ClPiCLskwxJRLzXOtcuv1Hk382Be6P96fvqXF72EjSv8E6bBAlLJvFaAeO3JH5JBsRJk3EZkPcu6abG2t1nGGQSCncOM667Eg3gvxAWcLGRrqUk1ePXL7YC9MfqBQbZf6A/h1RgRGNsgMKqvfq8_RYVeh0v8FyQDV8pR9ws4c0-Xt8",
#            folder_path="FUHT4zQL5Umz99BN7dUI/items",
#            filename="dA05K7d14K9Vo5tYqVE9.jpg",
#            bucket_name=bucketName)
