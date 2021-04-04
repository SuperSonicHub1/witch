from requests import Session
from gql import gql, Client
from gql.dsl import DSLSchema
from gql.transport.requests import RequestsHTTPTransport

session = Session()

transport = RequestsHTTPTransport(url="https://gql.twitch.tv/gql", headers={"Client-ID": "kimne78kx3ncx6brgo4mv6wki5h1ko"})

client = Client(transport=transport, fetch_schema_from_transport=True)

# Make a throwaway queryu to fetch the schema
client.execute(gql('{ user(login: "nyanners") { login } }'))

ds = DSLSchema(client.schema)
