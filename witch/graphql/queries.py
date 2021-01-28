import random
from typing import Dict, Union
from urllib.parse import urlencode
from sgqlc.endpoint.requests import RequestsEndpoint
from twitch_sgqlc import schema
from .operations import Operations
from ..session import session

endpoint = RequestsEndpoint(
    "https://gql.twitch.tv/gql",
    base_headers={"Client-ID": "kimne78kx3ncx6brgo4mv6wki5h1ko"},
    session=session,
)

base_steam_query: Dict[str, Union[str, int]]  = {
    "allow_source": "true",
    "allow_audio_only": "true",
    "allow_spectre": "true",
    "player": "twitchweb",
    "playlist_include_framerate": "true",
    "segment_preference": 4,
}


def get_live_streamer(login: str):
    op = Operations.query.get_live_user
    data = endpoint(op, dict(login=login))
    # Figure out why the operation syntax isn't working.
    # Figured it out: Twitch expects a RFC3339 timestamp. For example "2015-07-22T21:41:14Z".
    # while SGQLC assumes use of ISO 8601.
    # Only way I could fix this is by creating my own class. Hoo boy.
    # print(op + data)
    info = data["data"]
    access_token = info["user"]["stream"]["playbackAccessToken"]

    query = dict(**base_steam_query)
    query.update(
        {
            "p": random.randint(1000000, 10000000),
            "sig": access_token["signature"],
            "token": access_token["value"],
        }
    )
    return (
        info,
        f"https://usher.ttvnw.net/api/channel/hls/{login}.m3u8?{urlencode(query)}",
    )
