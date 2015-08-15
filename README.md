# paste

A super-simple pastebin app written in python using the Flask and redis-py libraries.

Front end uses jQuery.

## download

run `git clone https://github.com/ohnx/paste.git` to get the source. I only push runnable code.

## depend

Only 2 packages are depended upon.

Get them using `pip install redis Flask`

## configure

Configure how the URL shortener works in `app.py`

Line 8: change host='.' and port=6380 to the host and port of your redis setup

Line 11, 13, 15: Configures how a key is generated, the length of the key, possible characters to choose from when generating a key, and how many tries to generate a key.

Line 68: Debug mode on/off

Line 69: Open to public?

## run

`python app.py`

That's it!