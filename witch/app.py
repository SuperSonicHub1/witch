from flask import Flask, render_template, redirect, make_response, request, abort
from youtube_dl import YoutubeDL
from youtube_dl.utils import DownloadError
import requests
from mimetypes import guess_type
from . import default_settings

app = Flask(__name__)
app.config.from_object(default_settings)
app.config.from_envvar('WITCH_SETTINGS', silent=True)
ytdl = YoutubeDL({
    "quiet": True,
    # Activate quiet mode
    "source_address": "0.0.0.0",
    # Client-side IP address to bind to
    "dump_single_json": True,
    # Simulate, quiet but print JSON information for each command-line argument. If the URL refers to a playlist, dump the whole playlist information in a single line.
})
session = requests.Session()
session.headers.update({"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3535.2 Safari/537.36"})

@app.route("/favicon.ico")
def favicon():
    return redirect("https://static.twitchcdn.net/assets/favicon-32-d6025c14e900565d6177.png")

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
    try:
        info = ytdl.extract_info(f"https://twitch.tv/{streamer}/", download=False)
        return render_template("streamer.html.jinja2", streamer=streamer, info=info)
    except DownloadError as e:
        msg = str(e)
        if "does not exist" in msg:
            abort(404, f"{streamer} does not exist.")
        elif "is offline" in msg:
            abort(410, f"{streamer} is offline.")
        else:
            abort(500)
