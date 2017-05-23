import pdb            # Python Debugger
import time           # for sleep
import praw           # for reddit
import json           # for parsing json
import datetime       # time of the week
import gevent
from gevent import monkey
import pprint         # print stuff
import random         # for random user selection
from xml.dom import minidom        # for parsing XML

monkey.patch_all()
import urllib.request # for HTTP requests

d = datetime.datetime.now()
running_on_heroku = False

while True: # Always run
  if d.isoweekday() == 2: # 1 is monday | 7 is sunday ()

    if running_on_heroku: 
      reddit = praw.Reddit(
        user_agent='MyAnimeList Daily Bot v0.1',
        client_id='kBddA1U8dPkUtA',
        client_secret='SVFGuKd6hgpz2_X9UodRzjgpYvs',
        username='MAL-bot',
        password='Fox_MALbot_2002')
    else:
      print("Not running on Heroku!")
      break;

    subreddit = reddit.subreddit('malbottesting') # testing subreddit

    post = reddit.submission(id='6cg0vq') # A post on /r/malbottesting

    # Top Anime
    request = urllib.request.Request("https://www.matomari.tk/api/0.4/methods/anime.top.php", headers={'User-Agent': "Magic Browser"})
    connection = urllib.request.urlopen(request);
    anime_top_response_raw = connection.read()
    anime_top_response = json.loads(anime_top_response_raw.decode('utf-8'))

    # First random
    request = urllib.request.Request("https://www.matomari.tk/api/0.4/methods/anime.random.php", headers={'User-Agent': 'Magic Browser'})
    connection = urllib.request.urlopen(request)
    anime_random1_response_raw = connection.read();
    print(anime_random1_response_raw)
    anime_random1_response = json.loads(anime_random1_response_raw.decode('utf-8'))
    anime_random1_id = anime_random1_response["id"]

    # Second random
    request = urllib.request.Request("https://www.matomari.tk/api/0.4/methods/anime.random.php?not=" + str(anime_random1_id), headers={'User-Agent': 'Magic Browser'})
    connection = urllib.request.urlopen(request)
    anime_random2_response_raw = connection.read();
    print(anime_random2_response_raw)
    anime_random2_response = json.loads(anime_random2_response_raw.decode('utf-8'))
    anime_random2_id = anime_random2_response["id"]

    # Third random
    request = urllib.request.Request("https://www.matomari.tk/api/0.4/methods/anime.random.php?not=" + str(anime_random1_id) + "," + str(anime_random2_id), headers={'User-Agent': 'Magic Browser'})
    connection = urllib.request.urlopen(request)
    anime_random3_response_raw = connection.read();
    print(anime_random3_response_raw)
    anime_random3_response = json.loads(anime_random3_response_raw.decode('utf-8'))
    anime_random3_id = anime_random3_response["id"]

    # Fourth random
    request = urllib.request.Request("https://www.matomari.tk/api/0.4/methods/anime.random.php?not=" + str(anime_random1_id) + "," + str(anime_random2_id) + "," + str(anime_random3_id), headers={'User-Agent': 'Magic Browser'})
    connection = urllib.request.urlopen(request)
    anime_random4_response_raw = connection.read();
    print(anime_random4_response_raw)
    anime_random4_response = json.loads(anime_random4_response_raw.decode('utf-8'))
    anime_random4_id = anime_random4_response["id"]

    # Fifth random
    request = urllib.request.Request("https://www.matomari.tk/api/0.4/methods/anime.random.php?not=" + str(anime_random1_id) + "," + str(anime_random2_id) + "," + str(anime_random3_id) + "," + str(anime_random4_id), headers={'User-Agent': 'Magic Browser'})
    connection = urllib.request.urlopen(request)
    anime_random5_response_raw = connection.read();
    print(anime_random5_response_raw)
    anime_random5_response = json.loads(anime_random5_response_raw.decode('utf-8'))


    print("grabbing random person...")
    # Grab random person with flair
    flairs = []
    for flair in subreddit.flair(limit=None):
      flairs.append(flair)

    chosen_flair = random.choice(flairs);
    chosen_mal_username = chosen_flair["flair_text"].split("/")[-1]
    chosen_mal_username = chosen_mal_username.split("?")[0].split("#")[0]

    print(chosen_mal_username)

    while True:
      try:
        request = urllib.request.Request("https://www.matomari.tk/api/0.4/methods/user.info.USERNAME.php?username=" + chosen_mal_username, headers={'User-Agent': 'Magic Browser'})
        connection = urllib.request.urlopen(request)
      except urllib.error.HTTPError as e:
        if e.code == 404:
          chosen_flair = random.choice(flairs)
          chosen_mal_username = chosen_flair["flair_text"].split("/")[-1]
          chosen_mal_username = chosen_mal_username.split("?")[0].split("#")[-1]
      else:
        break;


    print("https://www.matomari.tk/api/0.3/user/info/" + chosen_mal_username + ".json")
    request = urllib.request.Request("https://www.matomari.tk/api/0.3/user/info/" + chosen_mal_username + ".json", headers={'User-Agent': 'Magic Browser'})
    connection = urllib.request.urlopen(request)
    user_list_response_raw = connection.read();
    print(user_list_response_raw)
    user_list_response = json.loads(user_list_response_raw.decode('utf-8'))

    user_favourites = {}


      
    # for anime in user_list_response["favourites"]["anime"]:
    def print_head(url):
      print('Starting download from ' + url)
      request = urllib.request.Request("https://www.matomari.tk/api/0.4/methods/anime.info.ID.php?id=" + anime, headers={'User-Agent': 'Magic Browser'})
      connection = urllib.request.urlopen(request)
      user_favourite_response_raw = connection.read()
      print(user_favourite_response_raw)
      user_favourites[anime] = json.loads(user_favourite_response_raw.decode('utf-8'));

    jobs = [gevent.spawn(print_head, anime) for anime in user_list_response["favourites"]["anime"]]

    gevent.joinall(jobs)

    pprint(jobs)
    print("favourites:")
    pprint(user_favourites)




    # submit(title, selftext=None, url=None resubmit=True, send_replies=True)
    # edit(body)
    post.edit("""#These are the top anime on MAL today!
^^Updated ^^""" + d.strftime('%Y-%m-%d') + """

---
## Top ranking anime
Rank | Score | Title
:--:|:--:|:--
""" +
str(anime_top_response["items"][0]["rank"]) + """ | """ + str(anime_top_response["items"][0]["score"]) + """ | [""" + anime_top_response["items"][0]["title"] + """](""" + anime_top_response["items"][0]["url"] + """) \n""" +
str(anime_top_response["items"][1]["rank"]) + """ | """ + str(anime_top_response["items"][1]["score"]) + """ | [""" + anime_top_response["items"][1]["title"] + """](""" + anime_top_response["items"][1]["url"] + """) \n""" +
str(anime_top_response["items"][2]["rank"]) + """ | """ + str(anime_top_response["items"][2]["score"]) + """ | [""" + anime_top_response["items"][2]["title"] + """](""" + anime_top_response["items"][2]["url"] + """) \n""" +
str(anime_top_response["items"][3]["rank"]) + """ | """ + str(anime_top_response["items"][3]["score"]) + """ | [""" + anime_top_response["items"][3]["title"] + """](""" + anime_top_response["items"][3]["url"] + """) \n""" +
str(anime_top_response["items"][4]["rank"]) + """ | """ + str(anime_top_response["items"][4]["score"]) + """ | [""" + anime_top_response["items"][4]["title"] + """](""" + anime_top_response["items"][4]["url"] + """) \n""" + """

---
## Random anime
Type | Score |Title
:--|:--:|:--
""" +
anime_random1_response["type"]  + """ | """ + str(anime_random1_response["score"]) + """ | [""" + anime_random1_response["title"] + """](""" + anime_random1_response["url"] + """) \n""" +
anime_random2_response["type"]  + """ | """ + str(anime_random2_response["score"]) + """ | [""" + anime_random2_response["title"] + """](""" + anime_random2_response["url"] + """) \n""" +
anime_random3_response["type"]  + """ | """ + str(anime_random3_response["score"]) + """ | [""" + anime_random3_response["title"] + """](""" + anime_random3_response["url"] + """) \n""" +
anime_random4_response["type"]  + """ | """ + str(anime_random4_response["score"]) + """ | [""" + anime_random4_response["title"] + """](""" + anime_random4_response["url"] + """) \n""" +
anime_random5_response["type"]  + """ | """ + str(anime_random5_response["score"]) + """ | [""" + anime_random5_response["title"] + """](""" + anime_random5_response["url"] + """) \n""" + """

---
## Today's random user is... """ + chosen_mal_username + """!
### """ + chosen_mal_username + """ ranks these anime highest! """


)
 
  time.sleep(300) # seconds
