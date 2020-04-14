from flask import Blueprint, jsonify, request
from Model.User import User
from Model.Project import Project
import json

project = Blueprint('project', __name__)


@project.route('/project/create', methods=['POST'])
def project_create():
    if request.method == 'POST':
        response = User.get_user_from_session(request.headers.get('SessionId'))
        if response['Status'] == 200:
            return Project.create_project(response['Message'], request.get_json())
    return json.dumps(response)


@project.route('/project/join', methods=['POST'])
def project_join():
    if request.method == 'POST':
        response = User.get_user_from_session(request.headers.get('SessionId'))
        if response['Status'] == 200:
            return Project.join_project(response['Message'], request.get_json()['ProjectId'])
    return json.dumps(response)


@project.route('/project/invite', methods=['POST'])
def project_invite():
    if request.method == 'POST':
        response = User.get_user_from_session(request.headers.get('SessionId'))
        if response['Status'] == 200:
            return Project.invite_to_project(request.get_json())
    return json.dumps(response)


@project.route('/project/leave', methods=['POST'])
def project_leave():
    if request.method == 'POST':
        response = User.get_user_from_session(request.headers.get('SessionId'))
        if response['Status'] == 200:
            return Project.leave_project(response['Message'], request.get_json()['ProjectId'])
    return json.dumps(response)


@project.route('/project/remove', methods=['POST'])
def project_remove():
    if request.method == 'POST':
        response = User.get_user_from_session(request.headers.get('SessionId'))
        if response['Status'] == 200:
            remove_info = request.get_json()
            return Project.remove_project(response['Message'], remove_info['ProjectId'], remove_info['Email'])
    return json.dumps(response)