# Witch
> A quick and sloppy Twitch alternative since Twitch killed Alternative Player for Twitch.tv, websites with embeds are dead, and the website itself is slow.

This project is powered by youtube-dl and Flask.

## Running
Clone the repository, `cd` into it, and assuming you have Poetry installed:
```shell
poetry install --no-dev 
# Now use your WSGI server of choice!
# I prefer Gunicorn.
gunicorn -w 4 witch:app
``` 

## Configuration
I make use of [Flask's configuration system](https://flask.palletsprojects.com/en/1.1.x/config/#configuring-from-files), using the environment variable `WITCH_SETTINGS`.
### `WEBSITE_ORIGIN`
__Default__: `"localhost"`

This is the full domain of the website you're hosting Witch on, for example: example.com. This is mostly used to make Twitch chat shut up.

## Roadmap
* ~~[Error handling](https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages/)~~
* ~~VODs~~
* ~~Clips~~
* Nice index
* Embeds
* Search
* Make pages more metadata rich
* Test suite
* CSS
