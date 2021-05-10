from datetime import datetime
from mimetypes import guess_type
from urllib.parse import urlparse
from flask import Flask, make_response, redirect, url_for, request, abort
from . import query
from .session import session
from .templated import templated

app = Flask(__name__)


@app.template_filter("datestr")
def datetime_to_string(s: str):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").strftime("%c UTC")


@app.route("/")
@templated()
def index():
    return {}

@app.route("/favicon.ico")
def favicon():
    return redirect(
        "https://static.twitchcdn.net/assets/favicon-32-d6025c14e900565d6177.png"
    )

###
# Section: Streamer
###


@app.route("/<streamer>/")
@templated()
def streamer(streamer: str):
    info, manifest, created_at = query.get_live_user(streamer)

    if not manifest:
        return redirect(url_for("streamer_profile", streamer=streamer))

    return {"info": info, "manifest": manifest, "created_at": created_at}


@app.route("/<streamer>/profile/")
@templated()
def streamer_profile(streamer: str):
    info = query.get_user(streamer)
    return {"info": info}


###
# Section: Public API
###


@app.route("/api/embed/<streamer>/")
@templated()
def embed_streamer(streamer: str):
    info, manifest, created_at = query.get_live_user(streamer)

    if not manifest:
        abort(410)

    return {"info": info, "manifest": manifest, "created_at": created_at}


###
# Section: Private API
###


@app.route("/api/goto/streamer")
def goto_streamer():
    return redirect(url_for("streamer", streamer=request.args.get("streamer")))


@app.route("/api/goto/url")
def goto_url():
    url = urlparse(request.args.get("url", ""))
    return redirect(url.path)


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
