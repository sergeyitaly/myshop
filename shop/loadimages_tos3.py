# shop/loadimages_tos3.py

import boto3
from botocore.exceptions import NoCredentialsError
import os
from dotenv import load_dotenv

class LoadImagesToS3:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    @staticmethod
    def upload_to_s3(local_file_path, s3_key):
        load_dotenv()

        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )

        try:
            s3_client.upload_file(local_file_path, os.getenv('AWS_STORAGE_BUCKET_NAME'), s3_key)
            print(f"Uploaded {local_file_path} to S3 bucket {os.getenv('AWS_STORAGE_BUCKET_NAME')} with key {s3_key}")
            return True
        except FileNotFoundError:
            print(f"File {local_file_path} not found.")
            return False
        except NoCredentialsError:
            print("AWS credentials not available.")
            return False

    @staticmethod
    def copy_local_media_to_s3(local_media_dir):
        """
        Recursively copies files from a local media directory to S3 under 'media/' prefix.
        """
        for root, dirs, files in os.walk(local_media_dir):
            for file in files:
                local_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_file_path, local_media_dir)

                # Construct S3 key with 'media/' prefix
                s3_key = f"media/{relative_path}"

                # Replace backslashes with forward slashes for S3 key (required on Windows)
                s3_key = s3_key.replace(os.path.sep, '/')

                # Upload the file to S3
                LoadImagesToS3.upload_to_s3(local_file_path, s3_key)
