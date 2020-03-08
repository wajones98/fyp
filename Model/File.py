import boto3
import os
from werkzeug.utils import secure_filename


class File:

    LANDING_FOLDER = '..\\fyp\\landing\\'
    BUCKET = 'fyp-data-repo'
    S3_CLIENT = boto3.client('s3')

    def __init__(self, file):
        self.file = file
        self.file_name = secure_filename(file.filename)
        self.full_path = os.path.join(self.LANDING_FOLDER, self.file_name)
        return

    def upload_file_landing(self):
        self.file.save(self.full_path)
        return self.full_path

    def delete_file_landing(self):
        os.remove(self.full_path)

    def upload_file_s3(self):
        return self.S3_CLIENT.upload_file(self.full_path, self.BUCKET, self.file_name)
