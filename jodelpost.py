__author__ = 'Jan'


from jodelrest import RESTClient


uni = {"latitude": 53.107, "longtitude": 8.853, "city": "Bremen"}
rc = RESTClient(uni, None)

print rc.post_image('pic.jpg').status_code
