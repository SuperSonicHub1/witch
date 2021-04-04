from gql.dsl import dsl_gql, DSLQuery
from .session import client, ds


def get_live_user(login: str):
    dsl_query = DSLQuery(
        ds.Query.user(login=login).select(
            ds.User.displayName,
            ds.User.broadcastSettings.select(
                ds.BroadcastSettings.title,
                ds.BroadcastSettings.game.select(ds.Game.boxArtURL, ds.Game.name),
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
                ds.Stream.viewersCount
            ),
        )
    )
    query = dsl_gql(dsl_query)
    return client.execute(query)



