from random import randint
from typing import Dict, Union, Tuple
from urllib.parse import urlencode
from gql.dsl import dsl_gql, DSLQuery
from .session import client, ds


def create_manifest_url(login: str, access_token: Dict[str, str]) -> str:
    base_stream_query: Dict[str, Union[str, int]] = {
        "allow_source": "true",
        "allow_audio_only": "true",
        "allow_spectre": "true",
        "player": "twitchweb",
        "playlist_include_framerate": "true",
        "segment_preference": 4,
    }

    query = dict(**base_stream_query)
    query.update(
        {
            "p": randint(1000000, 10000000),
            "sig": access_token["signature"],
            "token": access_token["value"],
        }
    )

    return f"https://usher.ttvnw.net/api/channel/hls/{login}.m3u8?{urlencode(query)}"


def get_live_user(login: str) -> Tuple[dict, str]:
    dsl_query = DSLQuery(
        ds.Query.user(login=login).select(
            ds.User.login,
            ds.User.displayName,
            ds.User.profileImageURL(width=300),
            ds.User.broadcastSettings.select(
                ds.BroadcastSettings.title,
                ds.BroadcastSettings.game.select(
                    ds.Game.boxArtURL(width=138, height=184), ds.Game.name
                ),
            ),
            ds.User.stream.select(
                ds.Stream.previewImageURL(width=1920, height=1080),
                ds.Stream.playbackAccessToken(
                    params={
                        "platform": "web",
                        "playerBackend": "mediaplayer",
                        "playerType": "site",
                    }
                ).select(
                    ds.PlaybackAccessToken.signature, ds.PlaybackAccessToken.value
                ),
                ds.Stream.viewersCount,
            ),
        )
    )
    query = dsl_gql(dsl_query)
    result = client.execute(query)
    if result["user"] and result["user"]["stream"]:
        manifest = create_manifest_url(
            login, result["user"]["stream"]["playbackAccessToken"]
        )
    else:
        manifest = ""

    return result, manifest
