# Witch
> A quick and sloppy Twitch alternative since Twitch killed Alternative Player for Twitch.tv, websites with embeds are dead, and the website itself is slow.

This project is powered by youtube-dl and Flask.

***THIS VERSION OF WITCH IS CURRENTLY BEING ABANDONED TO MOVE TO DIRECTLY WORKING WITH THE GRAPHQL API IN EARNEST, SWITCH TO A MORE FREINDLY VIDEO PLAYER, AND PRIORITIZE EASY NAVIGATION TO THE SITE. LOOK TO `new-branch` FOR THIS PROGRESS; IT WILL EVENTUALLY BECOME THE NEW MASTER.***

## Running
Clone the repository, `cd` into it, and assuming you have Poetry installed:
```shell
poetry install --no-dev 
# Now use your WSGI server of choice!
# I prefer Gunicorn.
gunicorn -w 4 witch:app
``` 

## Configuration
In order to make sure Twitch chat embeds for the time being work properly, make sure you change the website host. When using `flask run`, supply the host argument.

I make use of [Flask's configuration system](https://flask.palletsprojects.com/en/1.1.x/config/#configuring-from-files), using the environment variable `WITCH_SETTINGS`.


This is the full domain of the website you're hosting Witch on, for example: example.com. This is mostly used to make Twitch chat shut up.

## Roadmap
* ~~[Error handling](https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages/)~~
* ~~VODs~~
* ~~Clips~~
* ~~Nice index~~
* ~~Embeds~~
* Add a Makefile
* Search
* Make pages more metadata rich
* Fully migrate to Twitch GQL
* Add forms to `clips` and `videos` in order to allow users to filter results.
* Test suite
* CSS
