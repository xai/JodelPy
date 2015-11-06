from jodelpy import Location

__author__ = 'Jan'

class Location():

    def __init__(self, latitude, longtitude, name):
        self.latitude = latitude
        self.longtitude = longtitude
        self.name = name

    def __str__(self):
        return 'Lat : %s\nLong : %s\nName : %s' % (self.latitude, self.longtitude, self.name)


## Your Auth Token here
auth = 'Bearer xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

## Your Locations here

# home = Location(<Latitude>, <Longtitude>,<Name of the place>)

home = Location(12.34, 1.23456,"Somewhere")

## Don't change anything beyond this line if you don't know what you're doing!

COLORS = {'9EC41C','8ABDB0','FFBA00','DD5F5F','06A3CB', 'FF9908'}

USER_AGENT = 'Jodel/65000 Dalvik/2.1.0 (Linux; U; Android 5.1.1; Nexus 6 Build/1.0.001)'

headers = {"Connection":"keep-alive",
                "Authorization":auth,
                "User-Agent":USER_AGENT,
                "Accept-Encoding":"gzip",
                "Host":"api.go-tellm.com"}

post_headers = {"Connection":"keep-alive",
                "Authorization":auth,
                "User-Agent":USER_AGENT,
                "Accept-Encoding":"gzip",
                "Host":"api.go-tellm.com",
                "Content-Type":"application/json"}
