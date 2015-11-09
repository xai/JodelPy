import requests
import base64
import string
import random
import json

__author__ = 'Jan'

user_agent = 'Jodel/65000 Dalvik/2.1.0 (Linux; U; Android 5.1.1; D6503 Build/23.4.A.1.232)'

base_headers = {"Connection":"keep-alive",
                "User-Agent":user_agent,
                "Accept-Encoding":"gzip",
                "Host":"api.go-tellm.com",
                "Content-Type":"application/json; charset=UTF-8"}

auth = 'Bearer 4c512938-e33d-411e-84ff-cd8b97dc3945'



uni = {"latitude":53.1070074, "longtitude":8.85392980000006, "city":"Bremen"}


def create_header(doAuth = True):
    headers = base_headers
    if doAuth:
        headers['Authorization'] = auth
    return headers


def do_get(url):
    return requests.get(url, headers=create_header());


def do_put(url, payload):
    if payload is None:
        return requests.put(url, headers=create_header())

    return requests.put(url, data=payload, headers=create_header())


def do_delete(url):
    return requests.delete(url, headers=create_header())


def do_post(url, payload, doAuth=True):

    return requests.post(url, data=payload, headers=create_header(doAuth=doAuth))


def new_device_uid():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(63))


def get_access_token(place, latitude, longtitude, deviceuid=new_device_uid()):
    payload = {"client_id":"81e8a76e-1e02-4d17-9ba0-8a7020261b26",
               "device_uid":deviceuid,
               "location":
                   {"loc_accuracy":19.0,
                    "city":place,
                    "loc_coordinates":
                        {"lat":latitude,
                         "lng":longtitude},
                       "country":"DE"}
               }

    json_payload = json.dumps(payload)

    return do_post("https://api.go-tellm.com/api/v2/users/", json_payload, False).json()


def get_karma():
    return do_get("https://api.go-tellm.com/api/v2/users/karma").json()['karma']


def get_posts():
    return do_get("https://api.go-tellm.com/api/v2/posts/").json()['posts']


def get_posts_raw():
    return do_get("https://api.go-tellm.com/api/v2/posts/").content


def set_pos(longtitude, latitude, place, country="DE"):
    payload = {"location":
                   {"loc_accuracy":19.0,
                    "city": place ,
                    "loc_coordinates":
                        {"lat":latitude,
                         "lng":longtitude},
                    "country":country}
               }
    json_payload = json.dumps(payload)

    return do_put("https://api.go-tellm.com/api/v2/users/place", json_payload).content


def post(text, latitude, longtitude, place, country="DE", color="DD5F5F"):
    payload = {"color":color,
               "location":
                   {"loc_accuracy":10.0,
                    "city":place,
                    "loc_coordinates":
                        {"lat":latitude,
                         "lng":longtitude},
                    "country":country,
                    "name":"41"},
               "message":text
               }
    json_payload = json.dumps(payload)

    return do_post("https://api.go-tellm.com/api/v2/posts/", json_payload)


def delete(postid):
    return do_delete('https://api.go-tellm.com/api/v2/posts/%s' % postid).content


def post_image(file, latitude, longtitude, place, country="DE", color="DD5F5F"):
    with open(file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    payload = {"color":color,
               "image":encoded_string,
               "location":
                   {"loc_accuracy":10.0,
                    "city":place,
                    "loc_coordinates":
                        {"lat":latitude,
                         "lng":longtitude},
                    "country":country,
                    "name":"41"},
               "message":"photo"
               }
    json_payload = json.dumps(payload)
    return do_post("https://api.go-tellm.com/api/v2/posts/", json_payload)


def get_my_posts():
    return do_get("https://api.go-tellm.com/api/v2/posts/mine/").content


def upvote(postid):
    return do_put("https://api.go-tellm.com/api/v2/posts/%s/upvote" % postid, None).content


def downvote(postid):
    return do_put("https://api.go-tellm.com/api/v2/posts/%s/downvote" % postid, None).content


def new_acc(place, latitude, longtitude):
    access = get_access_token(place, latitude, longtitude)
    print access
    auth = "Bearer %s" % access['access_token']
    set_pos(longtitude, latitude, place)

posts = new_acc(home.name, home.latitude, home.longtitude)

