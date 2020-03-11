import boto3
import os

from Utils.Database import Database
from Utils import Common
from werkzeug.utils import secure_filename


class File:

    LANDING_FOLDER = '..\\fyp\\landing\\'
    BUCKET = 'fyp-data-repo'
    S3_CLIENT = boto3.client('s3')
    ALLOWED_EXTENSIONS = ('csv', 'mat')

    def __init__(self, file):
        self.file = file
        self.file_name = secure_filename(file.filename)
        self.full_path = os.path.join(self.LANDING_FOLDER, self.file_name)
        self.file_extension = os.path.splitext(self.file_name)[1]
        return

    def upload_file_landing(self):
        self.file.save(self.full_path)
        return self.full_path

    def delete_file_landing(self):
        os.remove(self.full_path)

    def upload_dataset_file_s3(self, directory):
        s3_path = f"{directory}/{Common.generate_unique_identifier()}-{self.file_name}"
        self.S3_CLIENT.upload_file(self.full_path, self.BUCKET, s3_path)
        return s3_path

    def upload_file_s3(self):
        s3_path = f"{Common.generate_unique_identifier()}-{self.file_name}"
        self.S3_CLIENT.upload_file(self.full_path, self.BUCKET, s3_path)
        return s3_path

    def check_file_extension(self):
        if self.file_extension in self.ALLOWED_EXTENSIONS:
            return {'Status': 403, 'Message': f'File extension "{self.file_extension}" forbidden'}
        else:
            return {'Status': 200, 'Message': f'File extension "{self.file_extension}" okay'}

    @staticmethod
    def check_for_dataset(file_id):
        query = f"""
                SELECT TOP 1 
                    [DataSet] 
                FROM    
                    [metadata].[File]
                WHERE
                    [FileID] = '{file_id}'
                """
        conn = Database.connect()
        cursor = conn.cursor()
        results = Database.execute_query(query, cursor)
        if not results:
            return {'Status': 500, 'Message': 'Could not find a dataset associated with this id'}
        else:
            return {'Status': 200, 'Message': results[0][0]}

