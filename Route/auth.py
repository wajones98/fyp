from flask import Blueprint, Flask, request
from Model.User import User as UserModel

auth = Blueprint('auth', __name__)


@auth.route('/auth/login', methods=['POST'])
def login():
    if request.method == 'POST':
        contents = request.get_json()
        session_id = UserModel.user_login(contents['Email'], contents['Password'])
        return {"session_id": session_id}


@auth.route('/auth/register', methods=['POST'])
def register():
    if request.method == 'POST':
        contents = request.get_json()
        user = UserModel.create_user_obj(contents)
        response = user.user_register()
        return {"Status": response}
