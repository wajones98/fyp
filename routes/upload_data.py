from flask import Blueprint, render_template

upload_data = Blueprint('upload_data', __name__)

@upload_data.route('/upload')
def upload_page():
    return render_template('upload_data.html')