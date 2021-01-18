from youtube_dl import YoutubeDL
from youtube_dl.utils import DownloadError
from flask import abort

ytdl = YoutubeDL({
    "quiet": True,
    # Activate quiet mode
    "source_address": "0.0.0.0",
    # Client-side IP address to bind to
    "dump_single_json": True,
    # Simulate, quiet but print JSON information for each command-line argument. If the URL refers to a playlist, dump the whole playlist information in a single line.
})

def attempt_extract(url: str, streamer: str = "") -> dict:
    """
    Attept to extract information from youtube-dl and abort with an error message if things go awry.
    """
    try:
        return ytdl.extract_info(url, download=False)
    except DownloadError as e:
        msg = str(e)
        if "does not exist" in msg:
            abort(404, f"{streamer} does not exist.")
        elif "is offline" in msg:
            abort(410, f"{streamer} is offline.")
        else:
            abort(500)
