import string
import random
import json
import base64

import requests

__author__ = 'Jan'


class RESTClient(object):
    BASE_HEADERS = {"Connection": "keep-alive",
                    "Accept-Encoding": "gzip",
                    "Content-Type": "application/json; charset=UTF-8"}

    uni = {"latitude": 53.107, "longtitude": 8.853, "city": "Bremen"}

    def new_device_uid(self):
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(63))

    def get_access_token(self, place, latitude, longtitude, ):
        payload = {"client_id": "81e8a76e-1e02-4d17-9ba0-8a7020261b26",
                   "device_uid": self.new_device_uid(),
                   "location":
                       {"loc_accuracy": 19.0,
                        "city": place,
                        "loc_coordinates":
                            {"lat": latitude,
                             "lng": longtitude},
                        "country": "DE"}
                   }

        json_payload = json.dumps(payload)

        return self.do_post("https://api.go-tellm.com/api/v2/users/", json_payload, False).json()

    def get_karma(self):
        return self.do_get("https://api.go-tellm.com/api/v2/users/karma").json()['karma']

    def get_posts(self):
        return self.do_get("https://api.go-tellm.com/api/v2/posts/").json()['posts']

    def get_posts_raw(self):
        return self.do_get("https://api.go-tellm.com/api/v2/posts/").content

    def do_delete(self, url):
        return requests.delete(url, headers=self.headers)

    def set_pos(self, longtitude, latitude, place, country="DE"):
        payload = {"location":
                       {"loc_accuracy": 19.0,
                        "city": place,
                        "loc_coordinates":
                            {"lat": latitude,
                             "lng": longtitude},
                        "country": country}
                   }
        json_payload = json.dumps(payload)

        return self.do_put("https://api.go-tellm.com/api/v2/users/place", json_payload).content

    def post(self, text, latitude, longtitude, place, country="DE", color="DD5F5F"):
        payload = {"color": color,
                   "location":
                       {"loc_accuracy": 10.0,
                        "city": place,
                        "loc_coordinates":
                            {"lat": latitude,
                             "lng": longtitude},
                        "country": country,
                        "name": "41"},
                   "message": text
                   }
        json_payload = json.dumps(payload)

        return self.do_post("https://api.go-tellm.com/api/v2/posts/", json_payload)

    def delete(self, postid):
        return self.do_delete('https://api.go-tellm.com/api/v2/posts/%s' % postid).content

    def post_image(self, file, latitude, longtitude, place, country="DE", color="DD5F5F"):
        with open(file, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        payload = {"color": color,
                   "image": encoded_string,
                   "location":
                       {"loc_accuracy": 10.0,
                        "city": place,
                        "loc_coordinates":
                            {"lat": latitude,
                             "lng": longtitude},
                        "country": country,
                        "name": "41"},
                   "message": "photo"
                   }
        json_payload = json.dumps(payload)
        return self.do_post("https://api.go-tellm.com/api/v2/posts/", json_payload)

    def get_my_posts(self):
        return self.do_get("https://api.go-tellm.com/api/v2/posts/mine/").content

    def upvote(self, postid):
        return self.do_put("https://api.go-tellm.com/api/v2/posts/%s/upvote" % postid, None).json()

    def downvote(self, postid):
        return self.do_put("https://api.go-tellm.com/api/v2/posts/%s/downvote" % postid, None).json()

    def new_acc(self, place, latitude, longtitude):
        access = self.get_access_token(place, latitude, longtitude)
        #print access
        self.set_pos(longtitude, latitude, place)
        return "Bearer %s" % access['access_token']

    def __init__(self, user_agent, auth=None):
        self.headers = dict(self.BASE_HEADERS)
        self.headers['User-Agent'] = user_agent
        if auth is None:
            auth = self.new_acc(self.uni['city'], self.uni['latitude'], self.uni['longtitude'])
        #print auth
        self.headers['Authorization'] = auth
        self.auth = auth

    def do_post(self, url, payload, doAuth=True):
        return requests.post(url, data=payload, headers=self.headers)

    def do_get(self, url):
        return requests.get(url, headers=self.headers);

    def do_put(self, url, payload=None):
        return requests.put(url, data=payload, headers=self.headers)

    def do_post(self, url, payload, do_auth=None):
        return requests.post(url, data=payload, headers=self.headers)

    def close(self):
        requests.session().close()

rc = RESTClient('Jodel/65000 Dalvik/2.1.0 (Linux; U; Android 5.1.1; D6503 Build/23.4.A.1.232)', None)
#rc.post("pic.png", rc.uni['latitude'], rc.uni['longtitude'], rc.uni['city'])
posts = rc.get_posts()
#print posts
#id = posts[0]['post_id']
#print "ID : %s" % id

rc.close()

for post in posts:
    print '(%s) %s' % (post['vote_count'], post['message'].encode('UTF-8'))
    var = str(raw_input("up / down  / nichts / delete / exit ?: "))

    commands = {'up', 'down', 'exit', 'comment', 'delete'}
    if var =='exit':
        break
    print 'Voting %s' % var

    id = post['post_id']

    print 'PostID : %s' % id

    if var not in commands:
        continue
    elif var =='exit':
        break
    else:
        if var != 'delete':
            amount = int(raw_input('Wie viel ? '))
        else:
            amount = int(post['vote_count']) + 5
            var = 'down'

        for i in range(1, amount + 1):
            rc = RESTClient('Jodel/65000 Dalvik/2.1.0 (Linux; U; Android 5.1.1; Nexus 6 Build/23.4.A)', None)
            if var == "up":
                try:
                    print 'Votes %s' % rc.upvote(id)['vote_count']
                except ValueError:
                    print "Vote Fehler!"
                    rc.close()
                    continue
            elif var == "down":
                try:
                    print 'Votes %s' % rc.downvote(id)['vote_count']
                except ValueError:
                    print "Vote Fehler!"
                    rc.close()
                    continue

            else:
                rc.close()
                continue
            rc.close()
