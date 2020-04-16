from flask import Flask, Blueprint, jsonify, request
from Utils.Common import generate_unique_identifier
from Model.Upload import Upload as Upload
from Model.File import File as FileModel
from Model.User import User as UserModel
import json

upload = Blueprint('upload', __name__)


@upload.route('/upload/metadata', methods=['POST'])
def upload_metadata():
    if request.method == 'POST':
        response = UserModel.get_user_from_session(request.headers.get('SessionId'))
        if response['Status'] == 200:
            user_id = response['Message']
            content = request.get_json()
            dataset_id = content['DataSetId']
            response = Upload.create_dataset_metadata(dataset_id, content['DataSetName'])
            if response['Status'] in (200, 201):
                for key in content['Tags'].keys():
                    Upload.upload_tags(dataset_id, key, content['Tags'].get(key))
                file_responses = []
                for file_id in content['Files'].keys():
                    metadata = Upload(file_id, content['Files'].get(file_id), user_id, content)
                    file_responses.append(metadata.upload_file_metadata())
                response['Files'] = file_responses
        return json.dumps(response)


@upload.route('/upload/files', methods=['POST'])
def upload_files():
    if request.method == 'POST':
        response = UserModel.get_user_from_session(request.headers.get('SessionId'))
        if response['Status'] == 200:
            submitted_files = request.files
            dataset_id = generate_unique_identifier()
            response = {'Status': 201, 'DataSetId': dataset_id, 'Files': []}
            for file in submitted_files.keys():
                file_id = generate_unique_identifier()
                file_obj = FileModel(submitted_files[file])
                file_valid_response = file_obj.check_file_extension()
                if file_valid_response['Status'] == 200:
                    file_obj.upload_file_landing()
                    file_path = file_obj.upload_dataset_file_s3(dataset_id, file_id)
                    if file_path is not None:
                        file_obj.delete_file_landing()
                        response['Files'].append({'FileId': file_id, 'FileName': file_obj.file_name,
                                                  'Message': 'Successfully uploaded'})
                    else:
                        response['Files'].append({'FileId': file_id, 'FileName': file_obj.file_name,
                                                  'Message': 'Could not upload to S3'})
                else:
                    response['Files'].append({'Status': file_valid_response['Status'],
                                              'FileId': file_id, 'Message': file_valid_response['Message']})
            return json.dumps(response)
        else:
            return response
