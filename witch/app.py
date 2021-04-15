from mimetypes import guess_type
from flask import Flask, make_response, redirect, url_for, request
from .templated import templated
from . import query
from .session import session


app = Flask(__name__)


@app.route("/")
@templated()
def index():
    return {}


###
# Section: Streamer
###


@app.route("/<streamer>/")
@templated()
def streamer(streamer: str):
    """TODO: if user not live, redirect to profile
    (https://m.twitch.tv/xqcow/profile)
    """

    info, manifest, created_at = query.get_live_user(streamer)
    return {"info": info, "manifest": manifest, "created_at": created_at}


###
# Section: Public API
###


@app.route("/api/embed/<streamer>/")
@templated()
def embed_streamer(streamer: str):
    """TODO: if user not live, return 410 (gone)"""

    info, manifest, created_at = query.get_live_user(streamer)
    return {"info": info, "manifest": manifest, "created_at": created_at}


###
# Section: Private API
###


@app.route("/api/goto/streamer")
def goto_streamer():
    return redirect(url_for("streamer", streamer=request.args.get("streamer")))


@app.route("/api/proxy/<path:url>")
def proxy(url: str):
    res = session.get(url)
    if ".m3u8" in url:
        content = res.text.replace("https://", "/api/proxy/https://")
        response = make_response(content)
        response.headers["content-type"] = "application/vnd.apple.mpegurl"
        response.headers["x-url"] = url
        return response
    elif ".ts" in url:
        response = make_response(res.content)
        response.headers["content-type"] = "video/MP2T"
        response.headers["x-url"] = url
        return response
    else:
        response = make_response(res.content)
        response.headers["content-type"] = guess_type(url)[0]
        response.headers["x-url"] = url
        return response
