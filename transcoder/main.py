import boto3
from secret_keys import SecretKeys
import subprocess

secret_keys = SecretKeys()


class VideoTranscoder:
    def __init__(self):
        self.s3_client = boto3.client(
            's3', 
            region_name=secret_keys.REGION_NAME,
            aws_access_key_id=secret_keys.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=secret_keys.AWS_SECRET_ACCESS_KEY,
        )

    def download_video(self, local_path):
        self.s3_client.download_file(
            secret_keys.S3_BUCKET, 
            secret_keys.S3_KEY, 
            local_path
        )

    def transcode_video(self, inout_path, output_dir):
        #HLS
        cmd = [
            
        ]


        subprocess.run()
    
        