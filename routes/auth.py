from flask import Blueprint, Flask, request
from Model.User import User as UserModel

auth = Blueprint('auth', __name__)


@auth.route('/auth/login', methods=['POST'])
def login():
    if request.method == 'POST':
        contents = request.get_json()
        user_id = UserModel.user_login(contents['Email'], contents['Password'])
        return {"user_id": user_id}
