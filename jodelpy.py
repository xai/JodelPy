import requests
import base64
import string
import random

from settings import headers, post_headers, home, uni, unauth_post_headers

__author__ = 'Jan'


def make_request(url):
    return requests.get(url, headers=headers);


def get_device_uid():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(63))


def get_access_token(place,latitude,longtitude,deviceuid=get_device_uid()):
    payload = '{"client_id":"81e8a76e-1e02-4d17-9ba0-8a7020261b26","device_uid":"'+deviceuid+'","location":{"loc_accuracy":19.0,"city":"'+place+'","loc_coordinates":{"lat":'+str(latitude)+',"lng":'+str(longtitude)+'},"country":"DE"}}'
    return requests.post("https://api.go-tellm.com/api/v2/users/", data=payload, headers=unauth_post_headers).json()['access_token']


def get_karma():
    return make_request("https://api.go-tellm.com/api/v2/users/karma").json()['karma']


def get_posts():
    return make_request("https://api.go-tellm.com/api/v2/posts/").json()['posts']


def get_posts_raw():
    return make_request("https://api.go-tellm.com/api/v2/posts/").content


def set_pos(longtitude, latitude, place, country="DE"):
    payload = "{\"location\":{\"loc_accuracy\":19.0,\"city\":\"%s\",\"loc_coordinates\":{\"lat\":%s,\"lng\":%s},\"country\":\"%s\"}}" % (place, latitude, longtitude, country)
    return requests.put("https://api.go-tellm.com/api/v2/users/place", data=payload, headers=post_headers).content


def post(text, latitude, longtitude, place, country="DE", color="DD5F5F"):
    payload = "{\"color\":\"%s\",\"location\":{\"loc_accuracy\":10.0,\"city\":\"%s\",\"loc_coordinates\":{\"lat\":%s,\"lng\":%s},\"country\":\"%s\",\"name\":\"41\"},\"message\":\"%s\"}" % (
        color, place, latitude, longtitude, country, text)
    return requests.post("https://api.go-tellm.com/api/v2/posts/", data=payload, headers=post_headers)


def delete(postid):
    return requests.delete('https://api.go-tellm.com/api/v2/posts/%s' % postid, headers=headers).content


def post_image(file, latitude, longtitude, place, country="DE", color="DD5F5F"):
    with open(file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    payload = "{\"color\":\"%s\",\"image\":\"%s\",\"location\":{\"loc_accuracy\":10.0,\"city\":\"%s\",\"loc_coordinates\":{\"lat\":%s,\"lng\":%s},\"country\":\"%s\",\"name\":\"41\"},\"message\":\"photo\"}" % (
        color,encoded_string, place, latitude, longtitude, country)
    return requests.post("https://api.go-tellm.com/api/v2/posts/", data=payload, headers=post_headers)


def get_my_posts():
    return make_request("https://api.go-tellm.com/api/v2/posts/mine/").content


def upvote(postid):
    requests.put("https://api.go-tellm.com/api/v2/posts/%s/upvote" % postid, headers=headers)


def downvote(postid):
    return requests.put("https://api.go-tellm.com/api/v2/posts/%s/downvote" % postid, headers=headers).content

#token = get_access_token(uni.name,uni.latitude,uni.longtitude)
#print token

#print auth
#print headers
#print get_karma()

#print set_pos(home.longtitude, home.latitude, home.name)
#print get_my_posts()
#delete('563eb04c17ad6933438fcc7b')
#print downvote("563ea157a9178fcc4d4e662b")
#print post_image("pic.jpg", home.latitude, home.longtitude, home.name).content
#upvote()
#print get_posts_raw()
