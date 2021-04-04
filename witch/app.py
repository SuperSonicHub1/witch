from flask import Flask
from .templated import templated
from . import query


app = Flask(__name__)

@app.route("/")
@templated()
def index():
    return {}

@app.route("/<streamer>/")
@templated()
def streamer(streamer: str):
    """TODO: if user not live, redirect to profile
    (https://m.twitch.tv/xqcow/profile)
    """

    info, manifest = query.get_live_user(streamer)

    return {"info": info, "manifest": manifest}