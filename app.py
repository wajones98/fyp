from flask import Flask, redirect
from Route.upload import upload
from Route.auth import auth
from Route.search import search
from Route.institution import institution
app = Flask(__name__)
app.debug = True

# Random os.urandom(16) secret key
app.secret_key = b'\x9a\xac\xea\x9e\xe9\xbbN\x1d\xa5\xb4\x1f\x17\xd3\xdd\x96O'

app.register_blueprint(upload)
app.register_blueprint(auth)
app.register_blueprint(search)
app.register_blueprint(institution)


@app.route('/')
def default():
    return redirect('https://github.com/wjones98/fyp')


if __name__ == '__main__':
    app.run()