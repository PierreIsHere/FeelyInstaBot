import os.path
from Login import api

try:
    from instagram_private_api import (
        Client, __version__ as client_version)
except ImportError:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from instagram_private_api import (
        Client, __version__ as client_version)

f = open("profanity.txt", "r")
profanity_list = [l[:-1] for l in f.readlines()]
f.close()

def scan(id):
    comments = api.media_n_comments(id, n=100, reverse=False)
    delete_queue = []
    try:
        for c in comments:
            for word in c['text'].split():
                if word.lower() in profanity_list:
                    print("Detected profanity in comment", c['pk'])
                    delete_queue.append(c['pk'])
                    break
        if len(delete_queue):
            api.bulk_delete_comments(id, delete_queue)
            delete_queue.clear()
    except IndexError:
        print("<no comments found>")

    print("Scanned post", id)