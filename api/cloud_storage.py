from google.cloud import storage

class CloudStorageManager:
    def __init__(self):
        self.storage_client = storage.Client()

    def upload_blob(self, bucket_name, source_file_name, destination_blob_name):
        
        #! Get the bucket and blob objects
        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        #! Upload the file to the specified blob
        blob.upload_from_filename(source_file_name)

        #! Print a success message
        print(
            "File {} uploaded to {}.".format(
                source_file_name, destination_blob_name
            )
        )

    def delete_all_blobs(self, bucket_name):
        #! Get the bucket object
        bucket = self.storage_client.bucket(bucket_name)

        #! Get a list of all blobs in the bucket
        blobs = bucket.list_blobs()

        #! Delete each blob in the bucket
        for blob in blobs:
            blob.delete()

        #! Print a success message
        print(f"All images in {bucket_name} were deleted.")