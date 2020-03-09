from flask import Flask, Blueprint, jsonify, request
from Model.Upload import Upload as UploadModel
from Model.File import File as FileModel
upload = Blueprint('upload', __name__)


@upload.route('/upload/metadata/<user_id>', methods=['POST'])
def upload_metadata(user_id):
    if request.method == 'POST':
        content = request.get_json()
        meta_obj = UploadModel(user_id, content)
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
