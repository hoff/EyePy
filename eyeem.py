#!/usr/bin/env python

"""
A Python wrapper for the EyeEm API4

Documentation at https://github.com/hoff/eyepy
"""

__author__ = 'micklinghoff@gmail.com'
__version__ = '0.1'

import requests
import logging

log_levels = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL
}
logger = logging.getLogger(__name__)

API_URL = "https://api.eyeem.com"
API_VERSION = "v2"

class API(object):
    def __init__(self, client_id, client_secret, callback_url, loglevel):
        self.api_url = API_URL
        self.version_id = API_VERSION
        self.client_id = client_id
        self.client_secret = client_secret
        self.callback_url = callback_url
        logging.basicConfig(level=log_levels[loglevel])
        self.base_payload = {'client_id': self.client_id}
        
    def create_auth_link(self):
        auth_link = "http://www.eyeem.com/oauth/authorize?response_type=code&client_id=%s&redirect_uri=%s" %(self.client_id, self.callback_url)
        return auth_link

    def get_authorization(self, code):
        """
        exchanges the code received from callback for an access token
        """
        path = "oauth/token"
        payload = self.base_payload
        payload['grant_type'] = "authorization_code"
        payload['client_id'] = self.client_id
        payload['client_secret'] = self.client_secret
        payload['redirect_uri'] = self.callback_url
        payload['code'] = code
        return self.make_request(path, payload)

    def make_request(self, path, data):
        """
        utility function to make requests agains a resource path with payload
        """
        url = "%s/%s/%s" %(self.api_url, self.version_id, path)
        payload = self.base_payload
        for k,v in data.iteritems():
            payload[k] = v
        req = requests.get(url, params=payload)
        logging.info("requesting %s" %(req.url))
        return req


    ##########
    # PHOTOS #
    ##########

    def get_photos(self, **kwargs):
        """
        Retrieves the authenticated user's latest twenty photos or popular photos (collection).
        The params type,date,frame/filter,ids are processed in that order. The first match is the source of the response.
        
        Optional arguments:
            type = "popular"
            date = 0
            interval = 1
            frame = 0
            filter = 0
            ids = None
            limit = 20
            offset  = 0
            detailed = 0
            includeComments = 0
            numComments = 2
            includeLikers = 0
            numLikers = 1
            includePeople = 0
            numPeople = 10
            includeAlbums = 0
            userDetails = 0
            simpleDescription = 0
        """
        payload = self.base_payload
        for k, v in kwargs.iteritems():
            payload[k] = v
        path = "photos"
        return self.make_request(path, payload)
 
    def get_photo_by_id(self, photo_id, **kwargs):
        """ 
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
        """
        payload = self.base_payload
        for k, v in kwargs.iteritems():
            payload[k] = v
        path = "photos/%d" %(photo_id)
        return self.make_request(path, payload)

    def get_popular_photos(self):
        """
        Return a collection of the current popular photos.
        """
        path = "photos/popular"
        return self.make_request(path, self.base_payload).json()

    def get_tagged_in_photo(self, photo_id):
        """
        Retrieves an array of people tagged in the photo
        Args: photo_id
        """
        path = "/photos/%d/people" %(photo_id)
        return self.make_request(path, self.base_payload).json()

    
    def get_photo_likers(self, photo_id):
        """
        Retrieves an array of the users who like the photo.
        Args: photo_id
        """
        path = "/photos/%d/likers" %(photo_id)
        return self.make_request(path, self.base_payload).json()

    def get_user_likes_photo(self, user_id, photo_id):
        """
        Checks whether a user likes a photo.
        Args: user_id, photo_id
        """
        path = "/photos/%d/likers/%d" %(photo_id, user_id)
        status_code = make_request(path, self.base_payload).status_code
        if status_code == 200:
            return True
        else:
            return False

    def get_photo_comments(self, photo_id):
        """
        Retrieves an array of a photo's comments.
        Args: photo_id
        """
        path = "/photos/%d/comments" %(photo_id)
        return self.make_request(path, self.base_payload)

    def get_comment_by_id(self, photo_id, comment_id):
        """
        Retrieves a specific comment on a photo.
        Args: photo_id, comment_id
        """
        path = "photos/%d/comments/%d" %(photo_id, comment_id)
        return self.make(path, self.base_payload)

    def get_photos_album(self, photo_id):
        """
        Retrieves an array of a photo's albums.
        Args: photo_id
        """
        path = "photos/%d/albums" %(photo_id)
        return self.make(path, self.base_payload)


    ############
    # DISCOVER #
    ############

    def discover(self, **kwargs):
        """
        Retrieves a dedicated discover feed - tailored to the user's preferences (or a generic one for non-authed endpoints)
        Optional arguments:
            limit = 30
            user_id = None
            offset= 0
            lat = None
            lng = None
            includePhotos = 1
            numPhotos = 6
            city  = None
            cc= None
            filter= None
        """
        payload = self.base_payload
        for k, v in kwargs.iteritems():
            payload[k] = v
        path = "discover"
        return self.make_request(path, payload)

    def discover_albums(self, **kwargs):
        """
        Retrieves a dedicated discover feed (made up ONLY of albums)
        tailored to the user's preferences (or a generic one for non-authed endpoints)
        
        optional arguments:
            limit = None
            offset = 0
            lat = None  
            lng = None
            includePhotos = 0
            numPhotos = 10
            includeContributors = 0
            includeLikers = 1
            filter = None 
            detailed = 0
        """
        path = "discover"
        payload = self.base_payload
        for k, v in kwargs.iteritems():
            payload[k] = v
        return self.make_request(path, payload)
        
    ##########
    # ALBUMS #
    ##########

    def get_albums(self, **kwargs):
        """
        Retrieves albums specified in the id URL query parameter, 
        or searches for albums based on their names.

        Optional arguments:
            detailed = 1
            includePhotos = 1
            numPhotos = 10
            includeContributors = 0
            includeLikers = 0
            offset = 0
            limit = 30
            q = None
            minPhotos = None
            type = None
            top = 0
            geoSearch = None
            lat = None
            lng = None
            foursquareId = None
            venueCategory = 0
            trending = 0
            ids = None
        """
        path = "albums"
        payload = self.base_payload
        for k, v in kwargs.iteritems():
            payload[k] = v
        return self.make_request(path, payload)

    def get_album_by_id(self, album_id, **kwargs):
        """
        Retrieves album by its id

        Required arguments:
            album_id
        Optional arguments:
            detailed=1
            includePhotos=0
            numPhotos=10
            includeContributors=0
            numContributors =30
            includeLikers=0
            numLikers=30
            photoDetails=0
            photoLikers=1
            photoNumLikers=1
            photoPeople=1
            photoNumPeople=1
            photoComments=1
            photoNumComments=1
            photoAlbums=1
            userDetails=0
        """
        path = "albums/%s" %(album_id)
        payload = self.base_payload
        for k, v in kwargs.iteritems():
            payload[k] = v
        return self.make_request(path, payload)

    def user_favorited_album(self, album_id, user_id):
        """
        Checks whether a user favorited an album.
        returns 200 if the user favorited the album, 404 otherwise

        Required arguments:
            album_id
            user_id
        """
        path = "albums/%d/favoriters/%d" %(album_id, user_id)
        status_code = make_request(path, self.base_payload).status_code
        if status_code == 200:
            return True
        else:
            return False

    def album_contributors(self, album_id, **kwargs):
        """
        Retrieves an array of the users who have added photos to the album.

        Required arguments:
            album_id
    
        Optional arguments:
            limit=20
            offset=0 
            onlyId=0 
            detailed=0 
        """
        path = "/albums/%d/contributors" %(album_id)
        payload = self.base_payload
        for k, v in kwargs.iteritems():
            payload[k] = v
        return self.make_request(path, payload)

    def album_photos(self, album_id):
        """
        required argument:
            album_id

        optional arguments:
            limit=20
            offset=0
            after=None
            before=None
            order=desc
            onlyId=0
            filter=None
            lat=None
            lng=None
            sort=chronological
            detailed=0
            includeComments=0
            numComments=2
            includeLikers=0
            numLikers=2
            includePeople=0
            numPeople=4
            includeAlbums=0
            userDetails=0
            simpleDescription=0 
        """
        path = "albums/%d/photos" %(album_id)
        payload = self.base_payload
        for k, v in kwargs.iteritems():
            payload[k] = v
        return self.make_request(path, payload)

    def photo_in_album(self, album_id, photo_id):
        """
        Checks whether a photo is in a particular album

        Required arguments:
            album_id
            photo_id
        """
        path = "albums/%d/photos/%d" %(album_id, photo_id)
        status_code = make_request(path, self.base_payload).status_code
        if status_code == 200:
            return True
        else:
            return False

    def related_albums(self, album_id, **kwargs):
        """
        Retrieves albums related to the one specified in the id URL query parameter. 
        Useful for finding popular topics at specific venues, cities in a country, etc...
        
        Required arguments:
            album_id

        Optional arguments:
            type=None
            venueCategory=0 
            limit=30
            offset=0 
        """
        path = "albums/%d/relatedAlbums" %(album_id)
        payload = self.base_payload
        for k, v in kwargs.iteritems():
            payload[k] = v
        return self.make_request(path, payload)
    

    
    def album_weather(self, album_id, **kwargs):
        """
        Retrieves the weather in a certain city.
        Works only for city/venue albums.

        Required arguments:
            album_id

        Optional arguments:
            date=TODAY (use format: YYYY-MM-DD)
        """
        path = "albums/%d/weather" %(album_id)
        payload = self.base_payload
        for k, v in kwargs.iteritems():
            payload[k] = v
        return self.make_request(path, payload)

    def album_venue_categories(self, album_id):
        """
        Retrieves the venueCategories of albums associated with a certain city/country/tag album.
        
        Required arguments:
            album_id
        """
        path = "albums/%d/venueCategories"
        return self.make_request(path, self.base_payload)

    def album_muted(self, album_id):
        """
        Check if a user has muted an album

        Required arguments:
            album_id
        """
        path = "albums/%d/mute" (album_id)
        return self.make_request(path, self.base_payload)

    def album_favoriters(self, album_id, **kwargs):
        """
        Retrieves an array of the users who favorited the album.

        Required arguments:
            album_id

        Optional arguments:
            limit=20
            offset=0 
        """
        path = "albums/%d/favoriters"
        payload = self.base_payload
        for k, v in kwargs.iteritems():
            payload[k] = v
        return self.make_request(path, payload)

    def albums_onboarding(self):
        """
        not implemented
        """
        raise NotImplementedError("This method is not implemented.")


    def collections(self):
        """
        Retrieves a collection of photos (at the moment, only "nearbyLive" is supported)
        NearbyLive is a mixture of photos uploaded very close to me w/in the last 2 hours + all nearby photos (geo-box)
        
        Optional arguments:
            type=None
            limit=30
            offset=0
            lat=X
            lng=X
            detailed=0
            includeComments=0
            numComments=2
            includeLikers=0
            numLikers=1
            includeAlbums=0
            includePeople=0
            numPeople=10
            simpleDescription=0
        """
        path = "collections"
        return self.make_request(path, self.base_payload)


    #########
    # USERS #
    #########

    def users(self, **kwargs):
        """
        Search for users or retrieve suggested users. either "suggested",or "q", or "ids".

        Optional arguments:
            suggested=0 
            q=None
            friends=0
            followers=0
            ids=None
            detailed=1
            limit=30
            offset=0
            action_id=None 

        Response: 200, pagination params and a array of user objects (either those queried, or those suggested)
        """
        path = "users"
        payload = self.base_payload
        for k, v in kwargs.iteritems():
            payload[k] = v
        return self.make_request(path, payload)

    def user_by_id(self, user_id, **kwargs):
        """
        Get a user's profile information. 
        Some parameters (liked settings, are only available to native clients.)

        Required arguments:
            user_id

        Optional arguments:
            detailed=1
            includePhotos=0
            numPhotos=10
            photoDetails=0
            photoLikers=1
            photoNumLikers=1
            photoPeople=1
            photoNumPeople=1
            photoComments=1
            photoNumComments=2
            photoAlbums=1
            includeSettings=0 

        Response:
            200 and a user object
        """
        path = "/users/%d" %(user_id)
        payload = self.base_payload
        for k, v in kwargs.iteritems():
            payload[k] = v
        return self.make_request(path, payload)

    def user_blocked_user(self, user_id, blocked_user_id):
        """
        check if the person (blocked_id) is blocked by the user (id)
        
        Required arguments:
            user_id
            blocked_user_id

        Response:
            Status code 200 if user is indeed blocked
        """
        path = "/users/%d/blocked/%d" %(user_id, block_user_id)
        status_code = make_request(path, self.base_payload).status_code
        if status_code == 200:
            return True
        else:
            return False

    def user_contacts(self, user_id, **kwargs):
        """
        Finds eyeem and social media (facebook, twitter) friends.
        Requires authed user.

        Required arguments:
            user_id

        Optional arguments:
            sm=0
            eyeem=0
            limit=20
            offset=0
            q=None
        """
        path = "users/%d/contacts" %(user_id)
        payload = self.base_payload
        for k, v in kwargs.iteritems():
            payload[k] = v
        return self.make_request(path, payload)


    def user_sm_contacts(self, user_id, **kwargs):
        # TODO: test or remove
        """
        Check social media accounts for friends (in eyeem, or to invite them)
        Requires authed user w/ native client.

        Required arguments:
            user_id
        Optional arguments:
            service=None
            matchContacts=0
            type=None
            detailed=1 
        """
        path = "users/%d/smContacts" %(user_id)
        payload = self.base_payload
        for k, v in kwargs.iteritems():
            payload[k] = v
        return self.make_request(path, payload)


    def user_fb_page(self, user_id, **kwargs):
        """
        Only available for the authenticated user,
        This call returns a service object with the Facebook pages of the user.

        Required arguments:
            user_id

        Optional arguments:
            page_id=None
        """
        path = "/users/%d/facebookPages" %(user_id)
        payload = self.base_payload
        for k, v in kwargs.iteritems():
            payload[k] = v
        return self.make_request(path, payload)


    def user_favorite_albums(self, user_id, **kwargs):
        """
        Get all the albums that a user has favorited.

        Required arguments:
            user_id

        Optional arguments:
            limit=20 
            offset=0 
            onlyId=0 
            detailed=1 
            includePhotos=0 
            numPhotos=7 
            includeContributors=0 
            includeLikers=0 
        """
        path = "users/%d/favoritedAlbums" %(user_id)
        payload = self.base_payload
        for k, v in kwargs.iteritems():
            payload[k] = v
        return self.make_request(path, payload)


    def user_feed(self, user_id, **kwargs):
        # todo: try out! ;)
        """
        Gets albums relevant to a user 
        Selection happens server side, includes albums they like, albums they contributed to, trending, recommended and nearby albums
        If requested from a user other than the authenticated one, only the user's liked albums are returned

        Required arguments:
            user_id

        Optional arguments:
            X-GEO-closestVenueFsIds=None
            X-GEO-cityName=None
            limit=20
            offset=0
            detailed=1
            includePhotos=1
            numPhotos=10
            includeContributors=0
            includeLikers=0 
        """
        path = "users/%d/feed" %(user_id)
        payload = self.base_payload
        for k, v in kwargs.iteritems():
            payload[k] = v
        return self.make_request(path, payload)


    def user_flags(self, user_id):
        """
        This call returns the user's chosen settings.
        Only available for the authenticated user.

        Required arguments:
            user_id
        """
        path = "users/%d/flags" %(user_id)
        return self.make_request(path, self.base_payload)


    def user_followers(self, user_id, **kwargs):
        """
        Get a user's followers.

        Required arguments:
            user_id
        Optional arguments:
            limit=20
            offset=0
            onlyId=None
            detailed=0 
        """
        path = "users/%d/followers" %(user_id)
        payload = self.base_payload
        for k, v in kwargs.iteritems():
            payload[k] = v
        return self.make_request(path, payload)

    def user_friends(self, user_id, **kwargs):
        """
        Get a user's friends (users that they follow)

        Required arguments:
            user_id

        Optional arguments:
            limit=20
            offset=0
            onlyId=None
            detailed=0 
        """
        path = "users/%d/friends" %(user_id)
        payload = self.base_payload
        for k, v in kwargs.iteritems():
            payload[k] = v
        return self.make_request(path, payload)

    def user_friends_photos(self, user_id, **kwargs):
        """
        Get all the photos by users that the given user follows (ordered chronologically).

        Required arguments:
            user_id

        Optional arguments:
            limit=30
            offset=0
            after=None
            before=None
            order=desc
            detailed=1
            includeComments=1
            numComments=2
            includeLikers=1
            numLikers=1
            includePeople=1
            numPeople=4
            includeAlbums=0
            userDetails=0
            simpleDescription=0 
        """
        path = "users/%d/friendsPhotos" %(user_id)
        payload = self.base_payload
        for k, v in kwargs.iteritems():
            payload[k] = v
        return self.make_request(path, payload)

    def users_are_friends(self, user_id, friend_id):
        """
        Check if the given user is friends with (follows) another user.

        Required arguments:
            user_id
            friend_id
        """
        path = "users/%d/friends/%d" %(user_id, friend_id)
        status_code = make_request(path, self.base_payload).status_code
        if status_code == 200:
            return True
        else:
            return False

    def user_liked_photos(self, user_id, **kwargs):
        """
        Get all the photos that a user has liked.

        Required arguments:
            user_id
        Optional arguments:
            limit=30
            offset=0
            onlyId=0
            detailed=1
            includeComments=1
            numComments=2
            includeLikers=1
            numLikers=1
            includePeople=1
            numPeople=4
            includeAlbums=0
            userDetails=0
            simpleDescription=0 
        """
        path = "users/%d/likedPhotos" %(user_id)
        payload = self.base_payload
        for k, v in kwargs.iteritems():
            payload[k] = v
        return self.make_request(path, payload)


    def user_photos(self, user_id, **kwargs):
        """
        Get the given user's photos, sorted chronologically (default).

        Required arguments:
            user_id
        Optional arguments:
            limit=30
            offset=0
            after=None
            before=None
            order=desc
            onlyId=0
            filter=None
            lat=None
            lng=None
            sort=chronological
            detailed=0
            includeComments=0
            numComments=2
            includeLikers=0
            numLikers=2
            includePeople=0
            numPeople=4
            includeAlbums=0
            simpleDescription=0 
        """
        path ="users/%d/photos" %(user_id)
        payload = self.base_payload
        for k, v in kwargs.iteritems():
            payload[k] = v
        return self.make_request(path, payload)

    def user_social_media(self, user_id):
        """
        Only available for the authenticated user.
        This call returns the status of the various connected social media accounts.

        Required arguments:
            user_id
        """
        path = "users/%d/socialMedia" %(user_id)
        payload = self.base_payload
        for k, v in kwargs.iteritems():
            payload[k] = v
        return self.make_request(path, payload)


    def user_follow_suggestions(self, user_id, **kwargs):
        """
        Get a list of suggested people to follow.

        Required arguments:
            user_id
        Optional arguments:
            service="all"
            detailed=0 
        """
        path = "users/%d/suggestions" %(user_id)
        payload = self.base_payload
        for k, v in kwargs.iteritems():
            payload[k] = v
        return self.make_request(path, payload)

    def user_topics(self, user_id, **kwargs):
        """
        Get a list of topics the user has contributed to (the topics correlate to tag albums).
        
        Required arguments:
            user_id
        Optional arguments:
            limit=20 VM1635:8
            offset=0 
        """
        path = "users/%d/topics" %(user_id)
        payload = self.base_payload
        for k, v in kwargs.iteritems():
            payload[k] = v
        return self.make_request(path, payload)


    ########
    # NEWS #
    ########

    def news(self, **kwargs):
        """
        Retrieves the authenticated user's news items (aggregated), either the latest items,
        or any items newer than newestId or any items older than oldestId.

        Optional arguments:
            limit=30
            oldestId=0
            newestId=0 
        """
        path = "news"
        payload = self.base_payload
        for k, v in kwargs.iteritems():
            payload[k] = v
        return self.make_request(path, payload)

    def news_by_id(self, news_id):
        """
        Required arguments:
            news_id

        Returns: 200 + news object 403 if requesting user isn't authorized to view the item 404 if the item doesn't exist
        """
        path = "news/%d" %(news_id)
        return self.make_request(path, self.base_payload)
        

    ##########
    # SEARCH #
    ##########

    def search_photos(self, **kwargs):
        """
        Retrieves an array containing photos

        Required arguments:
            q (string, the keyword to search)

        Optional arguments:
            limit=10 
            offset=0 
            user_id=None 
            album_id=None 
            detailed=1 
            includeComments=1 
            includeLikers=1 
            numComments=2 
            numLikers=1 
            includeAlbums=1 
            userDetails=0 
            includePeople=1 
            numPeople=10 
            simpleDescription=0
        """
        path = "search/photos"
        payload = self.base_payload
        for k, v in kwargs.iteritems():
            payload[k] = v
        return self.make_request(path, payload)


    def search_users_and_albums(self, **kwargs):
        """
        Retrieves an array containing a users and an albums dictionary.

        Required arguments:
            q (string, the keyword to search)

        Optional arguments:
            includeAlbums=0
            includeUsers=0
            limit=10
            offset=0 
        """
        path = "search"
        payload = self.base_payload
        for k, v in kwargs.iteritems():
            payload[k] = v
        return self.make_request(path, payload)

    def search_albums(self, **kwargs):
        """
        Retrieves an array containing albums.

        Required arguments:
            q (string, the keyword to search)

        Optional arguments:
            limit=10
            offset=0
            city_id=None
            album_type=None
            detailed=0 
        """
        path = "search/albums"
        payload = self.base_payload
        for k, v in kwargs.iteritems():
            payload[k] = v
        return self.make_request(path, payload)

    ##########
    # TOPICS #
    ##########

    def topics(self, **kwargs):
        """
        Retrieves an array containing a users and an albums dictionary.
        Auto-complete, https://api.eyeem.com/v2/topics?autoComplete=be
        returns dict of items containing "BE"

        Required arguments:
            autoComplete (string to auto-complete)
        """
        path = "topics"
        payload = self.base_payload
        for k, v in kwargs.iteritems():
            payload[k] = v
        return self.make_request(path, payload)


    ##########
    # VENUES #
    ##########

    def venue_fs_token(self):
        raise NotImplementedError("This method is available to EyeEm native clients only.")

    def venue_search(self, **kwargs):
        """
        Retrieves venues for a specific location and topics for each venue. 
        Additionally, the current city album is returned. 
        If the X-hourOfDay header is provided, topic suggestions are filtered according to their relevance (ex: breakfast in the morning, dinner at night)
        
        Required arguments:
            lat (float)
            lng (float)

        Optional arguments:
            cityName=None
            cc=None
            query=None 

        Example:
            https://api.eyeem.com/v2/venues/search?lat=52.2&lng=14.4
        """
        path = "venues/search"
        payload = self.base_payload
        for k, v in kwargs.iteritems():
            payload[k] = v
        return self.make_request(path, payload)