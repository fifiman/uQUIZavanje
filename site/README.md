# uQUIZavanje

### Learning Django

* [Official Django tutorial](https://docs.djangoproject.com/en/2.2/intro/tutorial01/), will probably be enough.

## Installation 

What is needed to run webserver:

1. Python 3 (>= 3.6)
2. Pip
3. Django, channels, channels-redis
4. redis-server

Python and pip installation instructions can be found online. Once you have python and pip, the needed python packages can be installed using `pip install Django channels channels-redis`. Check whether django is properly installed using `python -m django --version`. Redis-server can be installed on Ubuntu with `sudo apt install redis-server`. Windows users...google it.

## Running

A redis server must be started before running the django application.

In a seperate terminal window run: `redis-server` which will start redis on it's default port.

And then run `python manage.py runserver 0.0.0.0:8000`. 

## Source control

Everyone should have their own branch and only merge into the `master` branch with a pull request.  

[Git tutorials](https://gist.github.com/jaseemabid/1321592)
