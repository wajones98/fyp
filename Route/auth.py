from flask import Blueprint, request
from Model.User import User as UserModel
from flask_cors import CORS

auth = Blueprint('auth', __name__)

CORS(auth)


@auth.route('/auth/login', methods=['POST'])
def login():
    if request.method == 'POST':
        contents = request.get_json()
        response = UserModel.user_login(contents['Email'], contents['Password'])
        return response


@auth.route('/auth/register', methods=['POST'])
def register():
    if request.method == 'POST':
        contents = request.get_json()
        user = UserModel.create_user_obj(contents)
        response = user.user_register()
        return response
