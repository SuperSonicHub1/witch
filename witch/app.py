from flask import Flask, render_template, redirect, make_response, request
from .ytdl import ytdl, attempt_extract
import requests
from mimetypes import guess_type
from . import default_settings

app = Flask(__name__)
app.config.from_object(default_settings)
app.config.from_envvar("WITCH_SETTINGS", silent=True)

session = requests.Session()
session.headers.update(
    {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3535.2 Safari/537.36"
    }
)


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
    print(url, "\n", res.url)
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
