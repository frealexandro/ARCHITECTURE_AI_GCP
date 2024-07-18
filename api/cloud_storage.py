from google.cloud import storage


class CloudStorageManager:
    def __init__(self):
        self.storage_client = storage.Client()

    def upload_blob(self, bucket_name, source_file_name, destination_blob_name):
        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_filename(source_file_name)

        print(
            "File {} uploaded to {}.".format(
                source_file_name, destination_blob_name
            )
        )

    def delete_all_blobs(self, bucket_name):
        bucket = self.storage_client.bucket(bucket_name)

        blobs = bucket.list_blobs()
        for blob in blobs:
            blob.delete()

        print(f"Todas las imagenes {bucket_name} fueron eliminadas.")