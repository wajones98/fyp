from flask import Flask, Blueprint, jsonify, request
from Utils.Common import generate_unique_identifier
from Model.Upload import Upload as UploadModel
from Model.File import File as FileModel
from Model.User import User as UserModel
import json

upload = Blueprint('upload', __name__)


@upload.route('/upload/metadata/dataset', methods=['POST'])
def upload_dataset():
    if request.method == 'POST':
        content = request.get_json()
        user_id = UserModel.get_user_from_session(content['SessionID'])
        if user_id is not None:
            content = request.get_json()
            result = UploadModel.generate_dataset_id(content['DatasetName'])
            return result


@upload.route('/upload/metadata/file', methods=['POST'])
def upload_metadata():
    if request.method == 'POST':
        content = request.get_json()
        user_id = UserModel.get_user_from_session(content['SessionID'])
        if user_id != 'Session does not exist':
            content = request.get_json()
            meta_obj = UploadModel(user_id, content)
            response = meta_obj.upload_file_metadata()
            return response
    return {"Status": 500, "Message": user_id}


@upload.route('/upload/file/<file_id>', methods=['POST'])
def upload_file(file_id):
    if request.method == 'POST':
        files = request.files.getlist('file')
        file_obj = FileModel(files[0])
        file_obj.upload_file_landing()
        response = FileModel.check_for_dataset(file_id)
        if response['Status'] == 200:
            dataset_id = response['Message']
            file_path = file_obj.upload_dataset_file_s3(dataset_id)
        else:
            file_path = file_obj.upload_file_s3()
        UploadModel.update_init_file_path(file_id, file_path)
        file_obj.delete_file_landing()
        return {'Status': 201, 'FileID': file_id, 'FilePath': file_path}
    return {'Status': 500}


@upload.route('/upload/files', methods=['POST'])
def upload_files():
    if request.method == 'POST':
        response = UserModel.get_user_from_session(request.headers.get('SessionId'))
        if response['Status'] == 200:
            submitted_files = request.files.getlist('files')
            dataset_id = generate_unique_identifier()
            response = {'Status': 201, 'DataSetId': dataset_id, 'Files': []}
            for file in submitted_files:
                file_id = generate_unique_identifier()
                file_obj = FileModel(file)
                file_valid_response = file_obj.check_file_extension()
                if file_valid_response['Status'] == 200:
                    file_obj.upload_file_landing()
                    file_path = file_obj.upload_dataset_file_s3(dataset_id)
                    if file_path is not None:
                        UploadModel.update_init_file_landing(file_id, file_path)
                        file_obj.delete_file_landing()
                        response['Files'].append({'FileId': file_id, 'Message': 'Successfully uploaded'})
                    else:
                        response['Files'].append({'FileId': file_id, 'Message': 'Could not upload to S3'})
                else:
                    response['Files'].append({'FileId': file_id, 'Message': file_valid_response['Message']})
            return json.dumps(response)
        else:
            return response
    return {"Status": 405, "Message": 'Method not allowed'}
