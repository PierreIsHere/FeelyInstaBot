import json
import os.path
from Login import api
from badwords import badwords
from time import sleep

def jsonParser(dictName,col,badwords):
    arr = []
    temp = json.dumps([t[col] for t in dictName])
    temp = temp.replace("[","")
    temp = temp.replace("]","")
    temp = temp.split(", ")

    for i in temp:
        v = i.replace("\"","")
        bad = False
        for x in badwords:
            if v.lower() == x.lower():
                bad = True
                break
        if bad == False:
            arr.append(v)
    return arr


try:
    from instagram_private_api import (
        Client, __version__ as client_version)

except ImportError:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from instagram_private_api import (
        Client, __version__ as client_version)


rank_token = Client.generate_uuid()

#Getting the popular tags based off of search term
has_more = True
tsearch = input("Enter tag search term or enter 0 to skip: ")
limit = int(input("Enter number of tags: "))
tag_results = []

while has_more and rank_token and tsearch != 0 and len(tag_results) < 50:
    results = api.tag_search(tsearch, rank_token, exclude_list=[t['id'] for t in tag_results])
    tag_results.extend(results.get('results', []))
    has_more = results.get('has_more')
    rank_token = results.get('rank_token')

tags = jsonParser(tag_results,'name',badwords)
print(tags)
confirm = input("Confirm following the above hashtags(Y/n): ")
if confirm.lower() == "y":

    postList = []
    likeList = []
    if limit < len(tags):
        tags = tags[:limit]
    for tag in (tags):
        feed = api.feed_tag(tag,rank_token)
        posts = feed['ranked_items']
        for i in range(len(posts)-1): 
            postList.append(posts[i]["id"])

    for post in postList:
        likeList.append(api.media_likers(post))

    likeList=jsonParser(likeList,'users',badwords)    
    toFollow = []

    # print(likeList[1])
    x=1
    for i in range(0,(len(likeList)-1)):
        if "{pk:" in likeList[i]: 
            x =x+1
            temp = likeList[i]
            print(temp[5:])
            print(str(x)+".  "+likeList[i+1])
            # sleep(1)
            api.friendships_create(temp[5:])
            # tofollow.append(temp[5:])