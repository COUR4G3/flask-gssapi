from flask import Flask
from flask import render_template
from flask_gssapi import GSSAPI

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

gssapi = GSSAPI(app)

@app.route("/")
@app.route("/index")
@gssapi.require_auth
def index(username=''):
    return render_template('index.html', user=username)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)