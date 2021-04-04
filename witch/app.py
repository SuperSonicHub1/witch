from flask import Flask
from .templated import templated


app = Flask(__name__)

@app.route("/")
@templated()
def index():
    return {}
