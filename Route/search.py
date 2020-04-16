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
            search_builder = SearchModel(request.get_json())
            return search_builder.execute_search()
    return json.dumps(response)


@search.route('/download', methods=['GET'])
def download():
    if request.method == 'GET':
        response = UserModel.get_user_from_session(request.headers.get('SessionId'))
        if response['Status'] == 200:
            download_responses = []
            json_query = request.get_json()
            for file_path in json_query['Files']:
                download_responses.append(FileModel.download_file_s3(file_path, json_query['Local']))
    return json.dumps(download_responses)
