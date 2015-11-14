from jodelrest import RESTClient
from tqdm import *

__author__ = 'Jan'

uni = {"latitude": 53.107, "longtitude": 8.853, "city": "Bremen"}

rc = RESTClient(uni, None)
posts = rc.get_posts()
rc.close()

for post in posts:
    print '[ %s ] %s' % (post['vote_count'], post['message'].encode('UTF-8'))
    var = str(raw_input("[ up / down / exit ] : "))

    commands = {'up', 'down', 'exit'}

    if var == 'exit':
        break

    id = post['post_id']

    if var not in commands:
        continue
    elif var =='exit':
        break

    else:
        amount = int(raw_input('# Wie viel ? '))
        for i in tqdm(range(amount)):
            rc = RESTClient(uni, 'Jodel/65000 Dalvik/2.1.0 (Linux; U; Android 5.1.1; Nexus 6 Build/23.4.A)', None)
            try:
                if var == "up":
                    rc.upvote(id)
                elif var == "down":
                    rc.downvote(id)
            except ValueError:
                print "! Vote Fehler !"
                rc.close()

                continue
            rc.close()
        print '\n\n----------------------------\n'
