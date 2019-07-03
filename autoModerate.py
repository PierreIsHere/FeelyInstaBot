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
target_user_feed = api.user_feed(target_user_id)    # returns dictionary of posts
guarded_posts = {}

# store comment counts for all posts
# scans all comments
for post_id, c_count in [(p['pk'], p['comment_count']) for p in target_user_feed['items']]:
    scan(post_id)
    guarded_posts[post_id] = c_count

# continuously monitor stored posts for change in comment count
while True:
    has_changed = False
    for guarded_post_id in guarded_posts.keys():
        current_c_count = api.media_info(guarded_post_id)['items'][0]['comment_count']
        if current_c_count != guarded_posts[guarded_post_id]:
            has_changed = True
            scan(guarded_post_id)
            guarded_posts[guarded_post_id] = current_c_count

    if not has_changed: print("No new comments detected.")
    sleep(30)