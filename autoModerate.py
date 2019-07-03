import os.path
from time import sleep
from Login import api
from scanComments import scan

try:
    from instagram_private_api import (
        Client, __version__ as client_version)
except ImportError:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from instagram_private_api import (
        Client, __version__ as client_version)

target_user_id = '4155012351'
target_user_feed = api.user_feed(target_user_id)
guarded_posts = {}

# store number of posts
p_count = api.user_info(target_user_id)['user']['media_count']

# store comment counts for all posts
# scans all comments
for post_id, c_count in [(p['pk'], p['comment_count']) for p in target_user_feed['items']]:
    scan(post_id)
    guarded_posts[post_id] = c_count

# continuously monitor user feed
while True:
    has_changed = False
    # detects increase in post count
    if api.user_info(target_user_id)['user']['media_count'] > p_count:
        target_user_feed = api.user_feed(target_user_id)
        scan(target_user_feed['items'][0]['pk'])

    # detects change in comment count per post
    for guarded_post_id in guarded_posts.keys():
        current_c_count = api.media_info(guarded_post_id)['items'][0]['comment_count']
        if current_c_count != guarded_posts[guarded_post_id]:
            has_changed = True
            scan(guarded_post_id)
            guarded_posts[guarded_post_id] = current_c_count

    if not has_changed: print("No new comments detected.")
    sleep(30)