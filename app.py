from flask import Flask
from Routes.upload import upload
from Routes.auth import auth
app = Flask(__name__)
app.debug = True

# Random os.urandom(16) secret key
app.secret_key = b'\x9a\xac\xea\x9e\xe9\xbbN\x1d\xa5\xb4\x1f\x17\xd3\xdd\x96O'

app.register_blueprint(upload)
app.register_blueprint(auth)

if __name__ == '__main__':
    app.run()