![alt tag](http://eyeemapp.appspot.com/static/img/eyepy.png)

EyePy
=====

A simple Python wrapper for the EyeEm API (https://github.com/eyeem/Public-API)

HowTo:

Go to http://www.eyeem.com/developers/apps/list and create an app.

```python
import eyeem

CLIENT_ID = 'your_client_id'
CLIENT_SECRET  = 'your_client_secret'
CALLBACK_URL = 'your_oauth2_callback_url'
LOGLEVEL = 'info OR debug OR error'

api = eyeem.API(
    client_id     = CLIENT_ID,
    client_secret = CLIENT_SECRET,
    callback_url  = CALLBACK_URL,
    loglevel      = LOGLEVEL)
```


Some methods require oauth2 authorization.
To get an access token, generate a link to EyeEm like so:

```python
auth_link = api.create_auth_link()
```

and direct the user to that url. If she approves your app, she will be re-directed to your callback url with a "code" parameter.
Pick it up (e.g. 
```python
code = self.request.get("code") 
```
in app engine) and use it to generate an access token like so:

```python
access_token = api.get_authorization(code).json()['access_token']
```

At the time of writing, access token don't expire, so it's probably a good idea to store the token for each user so you don't have to send them through the hoops every time.

To use the access token in your API calls, simple pass it along with other parameters, like so:

```python
albums = api.discover_albums(limit=5, detailed=0, access_token=access_token).json()
```

All methods are documented with a description, required, and optional arguments.

```python
help(api.get_photo_by_id)

Retrieves a photo by id. 

Required argument:
    photo_id

Optional arguments:
    detailed  = 1
    includeComments = 1
    includeLikers = 1
    numComments = 2
    numLikers = 1
    includeAlbums = 1
    userDetails = 0
    includePeople = 1
    numPeople = 10
    simpleDescription = 0
```
Required arguments are always positional arguments, whereas optional arguments are always keyword arguments.


Note: This is a very early version of the wrapper, so stay tuned for updates.
