from flask import Flask, render_template, redirect, request, session, url_for
from routes.upload_data import upload_data
from routes.auth import auth
app = Flask(__name__)
app.debug = True

app.register_blueprint(upload_data)
app.register_blueprint(auth)


@app.route('/auth')
def main():
    return redirect('/auth')


@app.route('/upload-data')
def upload_data():
    return redirect(url_for('upload_data'))


if __name__ == '__main__':
    app.run()