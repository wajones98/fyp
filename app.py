from flask import Flask, render_template, redirect, request, session, url_for
from routes.upload_data import upload_data

app = Flask(__name__)
app.debug = True

app.register_blueprint(upload_data)

#UPLOAD_FOLDER = 'C:\\Users\\wajon\\OneDrive\\Documents\\GitHub\\fyp'
#app.secret_key = b'\x9c\xabH.\x96\x00\xd12\xf4\xab\xc0\xe6\xf8\x19P\x15'
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


@app.route('/')
def main():
    return render_template('home.html')


@app.route('/upload-data')
def upload_data():
    return redirect(url_for('upload_data'))


if __name__ == '__main__':
    app.run()