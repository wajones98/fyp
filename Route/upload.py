from flask import Flask, Blueprint, jsonify, request
from Model.Upload import Upload as UploadModel
from Model.File import File as FileModel
from Model.User import User as UserModel

upload = Blueprint('upload', __name__)


@upload.route('/upload/metadata/<session_id>', methods=['POST'])
def upload_metadata(session_id):
    if request.method == 'POST':
        user_id = UserModel.get_user_from_session(session_id)
        if user_id is not None:
            dataset_id = None
            content = request.get_json()
            if content['Dataset'] is not None:
                response = UploadModel.generate_dataset_id(content['Dataset'])
                if response['Status'] == 200:
                    dataset_id = response['DatasetID']
            meta_obj = UploadModel(user_id, content, dataset_id)
            response = meta_obj.upload_file_metadata()
            return response
    return {"Status": 500}


@upload.route('/upload/file/<file_id>', methods=['POST'])
def upload_file(file_id):
    if request.method == 'POST':
        files = request.files.getlist('file')
        file_obj = FileModel(files[0])
        file_path = file_obj.upload_file_landing()
        UploadModel.update_init_file_path(file_id, file_path)
        return {"Status": 201, "FileID": file_id, "FilePath": file_path}
    return {"Status": 500}
