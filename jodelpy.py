import requests

from settings import headers, post_headers, home

__author__ = 'Jan'

def make_request(url):
    return requests.get(url, headers=headers);


def get_karma():
    return make_request("https://api.go-tellm.com/api/v2/users/karma").json()['karma']


def get_posts():
    return make_request("https://api.go-tellm.com/api/v2/posts/").json()['posts']


def get_posts_raw():
    return make_request("https://api.go-tellm.com/api/v2/posts/").content


def set_pos(longtitude, latitude, place, country="DE"):
    payload = {
        "location": {"loc_accuracy": 1266.0, "city": place, "loc_coordinates": {"lat": latitude, "lng": longtitude},
                     "country": country}}
    requests.put("https://api.go-tellm.com/api/v2/users/place", data=payload, headers=headers)


def post(text, latitude, longtitude, place, country="DE", color="DD5F5F"):
    payload = "{\"color\":\"%s\",\"location\":{\"loc_accuracy\":10.0,\"city\":\"%s\",\"loc_coordinates\":{\"lat\":%s,\"lng\":%s},\"country\":\"%s\",\"name\":\"41\"},\"message\":\"%s\"}" % (
        color, place, latitude, longtitude, country, text)
    return requests.post("https://api.go-tellm.com/api/v2/posts/", data=payload, headers=post_headers)

def post_image(file, latitude, longtitude, place, country="DE", color="DD5F5F"):
    with open(file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    payload = "{\"color\":\"%s\",\"image\":\"%s\",\"location\":{\"loc_accuracy\":10.0,\"city\":\"%s\",\"loc_coordinates\":{\"lat\":%s,\"lng\":%s},\"country\":\"%s\",\"name\":\"41\"},\"message\":\"photo\"}" % (
        color,encoded_string, place, latitude, longtitude, country)
    return requests.post("https://api.go-tellm.com/api/v2/posts/", data=payload, headers=post_headers)

print get_karma()

set_pos(home.longtitude, home.latitude, home.name)

print post("Geht heute was ?", home.latitude, home.longtitude, home.place).content

print get_posts_raw()
