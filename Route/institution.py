from flask import Blueprint, jsonify, request
from Model.User import User
from Model.Institution import Institution
import json
institution = Blueprint('institution', __name__)


@institution.route('/institution/create', methods=['POST'])
def institution_create():
    if request.method == 'POST':
        response = User.get_user_from_session(request.headers.get('SessionId'))
        if response['Status'] == 200:
            user = User.get_user_info(response['Message'])
            if user.get_institution() is None:
                institution_info = request.get_json()
                institution_model = Institution()
                institution_model.set_name(institution_info['Name'])
                institution_model.set_desc(institution_info['Desc'])
                institution_model.set_owner(response['Message'])
                return Institution.create_institution(institution_model)
            return {'Status': 400, 'Message': 'Member already part of an institution'}
    return json.dumps(response)


@institution.route('/institution/join', methods=['POST'])
def institution_join():
    if request.method == 'POST':
        response = User.get_user_from_session(request.headers.get('SessionId'))
        if response['Status'] == 200:
            institution_invitation = request.get_json()
            return Institution.accept_pending_invite(response['Message'], institution_invitation['InstitutionId'])
    return json.dumps(response)


@institution.route('/institution/invite', methods=['POST'])
def institution_invite():
    if request.method == 'POST':
        response = User.get_user_from_session(request.headers.get('SessionId'))
        if response['Status'] == 200:
            invitation_info = request.get_json()
            return Institution.invite_member(response['Message'], invitation_info)
    return json.dumps(response)


@institution.route('/institution/remove', methods=['POST'])
def institution_remove():
    if request.method == 'POST':
        response = User.get_user_from_session(request.headers.get('SessionId'))
        if response['Status'] == 200:
            remove_info = request.get_json()
            return Institution.remove_member(response['Message'], remove_info['Email'])
    return json.dumps(response)


@institution.route('/institution/leave', methods=['POST'])
def institution_leave():
    if request.method == 'POST':
        response = User.get_user_from_session(request.headers.get('SessionId'))
        if response['Status'] == 200:
            return Institution.member_leave(response['Message'])
    return json.dumps(response)