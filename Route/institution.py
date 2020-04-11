from flask import Blueprint, jsonify, request

institution = Blueprint('institution', __name__)


@institution.route('institution/create', methods=['POST'])
def institution_create():
    return None


@institution.route('institution/join', methods=['POST'])
def institution_join():
    return None


@institution.route('institution/remove', methods=['POST'])
def institution_remove():
    return None


@institution.route('institution/delete', methods=['POST'])
def institution_create():
    return None


@institution.route('institution/leave', methods=['POST'])
def institution_leave():
    return None