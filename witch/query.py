from datetime import datetime
from random import randint
from typing import Dict, Union, Tuple
from urllib.parse import urlencode
from gql.dsl import dsl_gql, DSLQuery
from .session import client, ds


def get_user(login: str):
    game_fragment = (ds.Game.name, ds.Game.boxArtURL(width=138 / 2, height=184 / 2))

    videos_fragment = ds.VideoConnection.edges.select(
        ds.VideoEdge.node.select(
            ds.Video.viewCount,
            ds.Video.title,
            ds.Video.publishedAt,
            ds.Video.previewThumbnailURL(width=260, height=147),
            ds.Video.game.select(*game_fragment),
        )
    )

    dsl_query = DSLQuery(
        ds.Query.user(login=login).select(
            ds.User.login,
            ds.User.displayName,
            ds.User.profileImageURL(width=50),
            ds.User.bannerImageURL,
            ds.User.broadcastSettings.select(
                ds.BroadcastSettings.game.select(ds.Game.name)
            ),
            ds.User.stream.select(ds.Stream.viewersCount),
            ds.User.clips.select(
                ds.ClipConnection.edges.select(
                    ds.ClipEdge.node.select(
                        ds.Clip.curator.select(ds.User.displayName, ds.User.login),
                        ds.Clip.createdAt,
                        ds.Clip.viewCount,
                        ds.Clip.id,
                        ds.Clip.title,
                        ds.Clip.game.select(*game_fragment),
                        ds.Clip.thumbnailURL(width=260, height=147),
                    )
                )
            ),
            videos=ds.User.videos(type="ARCHIVE").select(videos_fragment),
            highlights=ds.User.videos(type="HIGHLIGHT").select(videos_fragment),
        )
    )

    query = dsl_gql(dsl_query)
    result = client.execute(query)

    return result


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


def get_live_user(login: str) -> Tuple[dict, str, str]:
    dsl_query = DSLQuery(
        ds.Query.user(login=login).select(
            ds.User.login,
            ds.User.displayName,
            ds.User.profileImageURL(width=50),
            ds.User.broadcastSettings.select(
                ds.BroadcastSettings.title,
                ds.BroadcastSettings.game.select(
                    ds.Game.boxArtURL(width=138 / 2, height=184 / 2),
                    ds.Game.displayName,
                    ds.Game.name,
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
                ds.Stream.createdAt,
            ),
        )
    )
    query = dsl_gql(dsl_query)
    result = client.execute(query)

    manifest = ""
    created_at = ""

    if result["user"] and result["user"]["stream"]:
        manifest = create_manifest_url(
            login, result["user"]["stream"]["playbackAccessToken"]
        )
        created_at = datetime.strptime(
            result["user"]["stream"]["createdAt"], "%Y-%m-%dT%H:%M:%SZ"
        ).strftime("%c")

    return result, manifest, created_at
