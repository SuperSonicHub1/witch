import random
from typing import Dict, Union, Tuple
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


def get_live_streamer(login: str) -> Tuple[schema.Query, str]:
    op = Operations.query.get_live_user
    data = endpoint(op, dict(login=login))
    info: schema.Query = (op + data)
    access_token = info.user.stream.playback_access_token

    query = dict(**base_steam_query)
    query.update(
        {
            "p": random.randint(1000000, 10000000),
            "sig": access_token.signature,
            "token": access_token.value,
        }
    )
    return (
        info,
        f"https://usher.ttvnw.net/api/channel/hls/{login}.m3u8?{urlencode(query)}",
    )
