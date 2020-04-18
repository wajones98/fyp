from flask import Blueprint, jsonify, request
from Model.SearchResult import Search as SearchModel
from Model.User import User as UserModel
from Model.File import File as FileModel

import json

search = Blueprint('search', __name__)


@search.route('/search', methods=['POST'])
def search_for():
    if request.method == 'POST':
        response = UserModel.get_user_from_session(request.headers.get('SessionId'))
        if response['Status'] == 200:
            search_type = None
            if 'Private' in request.headers:
                search_type = request.headers.get('Private')
            search_builder = SearchModel(request.get_json(), search_type)
            return search_builder.execute_search()
    return json.dumps(response)


@search.route('/download/file', methods=['POST'])
def download_file():
    if request.method == 'POST':
        response = UserModel.get_user_from_session(request.headers.get('SessionId'))
        if response['Status'] == 200:
            json_query = request.get_json()
            return FileModel.download_file_s3(json_query['File'])
    return json.dumps(response)
