from flask import Flask, Blueprint, jsonify, request
from Model.Upload import Upload as UploadModel
from Model.File import File as FileModel
from Model.User import User as UserModel

upload = Blueprint('upload', __name__)


@upload.route('/upload/metadata/dataset/<session_id>', methods=['POST'])
def upload_dataset(session_id):
    if request.method == 'POST':
        user_id = UserModel.get_user_from_session(session_id)
        if user_id is not None:
            content = request.get_json()
            result = UploadModel.generate_dataset_id(content['DatasetName'])
            return result


@upload.route('/upload/metadata/<session_id>', methods=['POST'])
def upload_metadata(session_id):
    if request.method == 'POST':
        user_id = UserModel.get_user_from_session(session_id)
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
