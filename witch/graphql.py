from sgqlc.endpoint.requests import RequestsEndpoint
from sgqlc.operation import Operation
from twitch_sgqlc import schema
from .session import session

endpoint = RequestsEndpoint(
    "https://gql.twitch.tv/gql",
    base_headers={"Client-ID": "kimne78kx3ncx6brgo4mv6wki5h1ko"},
    session=session,
)

def get_live_streamer(login: str):
    op = Operation(schema.Query)
    