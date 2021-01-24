from flask import Flask, render_template, redirect, make_response, request, url_for
from .ytdl import ytdl, attempt_extract
from mimetypes import guess_type
from .session import session
from . import default_settings

app = Flask(__name__)
app.config.from_object(default_settings)
app.config.from_envvar("WITCH_SETTINGS", silent=True)

@app.route("/favicon.ico")
def favicon():
    return redirect(
        "https://static.twitchcdn.net/assets/favicon-32-d6025c14e900565d6177.png"
    )


@app.route("/")
def index():
    return "Go to /{streamer}/ to find the person you want to watch."


@app.route("/api/proxy/<path:url>")
def proxy(url: str):
    res = session.get(url)
    if ".m3u8" in url:
        content = res.text.replace("https://", "/api/proxy/https://")
        response = make_response(content)
        response.headers["content-type"] = "application/vnd.apple.mpegurl"
        return response
    else:
        response = make_response(res.content)
        response.headers["content-type"] = guess_type(url)[0]
        return response


@app.route("/<streamer>/")
def streamer(streamer: str):
    info = attempt_extract(f"https://twitch.tv/{streamer}/", streamer=streamer)
    return render_template("streamer.html.jinja2", streamer=streamer, info=info)


@app.route("/<streamer>/videos/")
def videos(streamer: str):
    qs: bytes = request.query_string
    # Add forms
    info = attempt_extract(f"https://twitch.tv/{streamer}/videos/?{qs.decode('ascii')}", streamer=streamer)
    return render_template("videos.html.jinja2", streamer=streamer, info=info)


@app.route("/<streamer>/clips/")
def clips(streamer: str):
    qs: bytes = request.query_string
    # Add forms
    info = attempt_extract(f"https://twitch.tv/{streamer}/clips?{qs.decode('ascii')}", streamer=streamer)
    return render_template("clips.html.jinja2", streamer=streamer, info=info)


@app.route("/<streamer>/clip/<id_>")
def streamer_clip(streamer: str, id_: str):
    return redirect(url_for("clip", id_=id_))

@app.route('/clips/<id_>')
def clip(id_: str):
    info = attempt_extract(f"https://clips.twitch.tv/{id_}")
    return render_template("clip.html.jinja2", streamer=streamer, info=info)

@app.route("/videos/<int:id_>/")
def vod(id_: int):
    info = attempt_extract(f"https://twitch.tv/videos/{id_}/")
    return render_template("vod.html.jinja2", info=info)
