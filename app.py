from flask import Flask, render_template, redirect, request, session, url_for
from routes.upload_data import upload_data
app = Flask(__name__)
app.debug = True

app.register_blueprint(upload_data)

@app.route('/')
def main():
    return render_template('home.html')


@app.route('/upload-data')
def upload_data():
    return redirect(url_for('upload_data'))


if __name__ == '__main__':
    app.run()