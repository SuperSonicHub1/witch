import requests

session = requests.Session()
session.headers.update(
    {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3535.2 Safari/537.36"
    }
)
