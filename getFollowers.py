import json
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

# ---------- Pagination with max_id ----------
user_id = input("Enter a user ID: ")
followers = []
rank_token = Client.generate_uuid()
results = api.user_followers(user_id, rank_token)
followers.extend(results.get('users', []))

next_max_id = results.get('next_max_id')
while next_max_id:
    results = api.user_followers(user_id, rank_token, max_id=next_max_id)
    followers.extend(results.get('users', []))
    if len(followers) >= 600:    # get only first 600 or so
        break
    next_max_id = results.get('next_max_id')

followers.sort(key=lambda x: x['pk'])
# print list of user IDs
print(json.dumps([u['pk'] for u in followers], indent=2))

feed = api.feed_tag("pianoschool",rank_token)
posts = feed['ranked_items']

for i in range(len(posts)-1): 
    print(posts[i]["id"])
print
feed = api.feed_tag("pianoschool",rank_token)
posts = feed['ranked_items']

for i in range(len(posts)-1): 
    print(posts[i]["id"])