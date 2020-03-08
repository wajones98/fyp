import boto3
import os
from flask import Blueprint, render_template, request
from models import File as file_model

upload_data = Blueprint('upload_data', __name__)


@upload_data.route('/upload')
def upload_page():
    return render_template('upload_data.html')


@upload_data.route('/upload/submit', methods=['GET', 'POST'])
def submit_files():
    if request.method == 'POST':

        data_files = request.files.getlist('file[]')

        for data_file in data_files:
            file = file_model.File(data_file)
            file.upload_file_landing()
            #file.upload_file_s3()
            #file.delete_file_landing()

        return render_template('upload_data.html')