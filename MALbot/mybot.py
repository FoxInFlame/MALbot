# -*- coding: utf-8 -*-

import pdb                   # Python Debugger
import sys                   # system related stuff
import os                    # os related stuff
import pprint                # print stuff
import random                # for random user selection
import gevent                # syncrhonous loop api
from gevent import monkey    # for monkey patching
monkey.patch_all()           # make sure to monkey patch before importing praw
# <pokechu22> But at least it makes a suggestion - try doing the monkey patching before you import praw/anything else (would be a stupid workaround, but it might work)
# https://github.com/kennethreitz/requests/issues/3752

import time                  # for sleepin'
from apscheduler.schedulers.blocking import BlockingScheduler
import praw                  # for reddit API
import xmltodict             # xml to json | fast as well :)
import json                  # for parsing json
import datetime              # time of the week
import urllib.request        # for more HTTP requests

d = datetime.datetime.now()  # set current date as d to check weekday

def scheduled_job(): # will call at the bottom
  str(datetime.datetime.now()) # output datetime so we can know.
  #if d.isoweekday() == 3: # 1 is monday | 7 is sunday ()

  reddit = praw.Reddit(
    user_agent='MyAnimeList Daily Bot v0.1',
    client_id='kBddA1U8dPkUtA',
    client_secret='SVFGuKd6hgpz2_X9UodRzjgpYvs',
    username=os.environ['REDDIT_USERNAME'],
    password=os.environ['REDDIT_PASSWORD'])
  
  subreddit = reddit.subreddit('MyAnimeList') # testing subreddit

  post = reddit.submission(id='6d5wyk') # A post on /r/malbottesting

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
  print("https://www.matomari.tk/api/0.4/methods/anime.random.php?not=" + str(anime_random1_id) + "," + str(anime_random2_id) + "," + str(anime_random3_id) + "," + str(anime_random4_id))
  request = urllib.request.Request("https://www.matomari.tk/api/0.4/methods/anime.random.php?not=" + str(anime_random1_id) + "," + str(anime_random2_id) + "," + str(anime_random3_id) + "," + str(anime_random4_id), headers={'User-Agent': 'Magic Browser'})
  connection = urllib.request.urlopen(request)
  anime_random5_response_raw = connection.read();
  print(anime_random5_response_raw)
  anime_random5_response = json.loads(anime_random5_response_raw.decode('utf-8'))


  print("Grabbing random person...")
  # Grab random person with flair
  flairs = []
  for flair in subreddit.flair():
    flairs.append(flair)

  chosen_flair = random.choice(flairs);
  chosen_mal_username = chosen_flair["flair_text"].split("/")[-1]
  chosen_mal_username = chosen_mal_username.split("?")[0].split("#")[0]

  print("Chosen username:")
  print(chosen_mal_username)

  def checkProfileExists(username):
    try:
      print("Checking if profile exists...")
      request = urllib.request.Request("https://www.matomari.tk/api/0.4/methods/user.info.USERNAME.php?username=" + username, headers={'User-Agent': 'Magic Browser'})
      connection = urllib.request.urlopen(request) # No need to store response, it's just for testing connection
    except urllib.error.HTTPError as e:
      if e.code == 404: # Doesn't exist
        print("Username doesn't exist... trying new one:")
        chosen_flair = random.choice(flairs) # New random
        chosen_mal_username = chosen_flair["flair_text"].split("/")[-1]
        chosen_mal_username = chosen_mal_username.split("?")[0].split("#")[-1]
        checkProfileExists(chosen_mal_username)
      else:
        print("user.info.USERNAME returned an error othan than 404!")
        return;
  checkProfileExists(chosen_mal_username)

  endpoints = [
    "https://www.matomari.tk/api/0.3/user/info/" + chosen_mal_username + ".json",
    "https://www.matomari.tk/api/0.3/general/malappinfo.php?u=" + chosen_mal_username + "&type=anime&status=all"
  ]

  user_response = {}

  def getInfoFromUsername(endpoint):
    print('Starting download from ' + endpoint)
    request = urllib.request.Request(endpoint, headers={'User-Agent': 'Magic Browser'})
    connection = urllib.request.urlopen(request)
    if("malappinfo" in endpoint):
      user_list_response_raw = connection.read()
      user_response["user_list_response"] = xmltodict.parse(user_list_response_raw)
    else:
      user_profile_response_raw = connection.read()
      user_response["user_profile_response"] = json.loads(user_profile_response_raw.decode('utf-8'))
     
  jobs = [gevent.spawn(getInfoFromUsername, endpoint) for endpoint in endpoints]

  gevent.joinall(jobs)



  user_favourites = {}
    
  # for anime in user_profile_response["favourites"]["anime"]:
  def favouriteToArray(id):
    print('Starting to download anime info: ' + id)
    request = urllib.request.Request("https://www.matomari.tk/api/0.4/methods/anime.info.ID.php?id=" + id, headers={'User-Agent': 'Magic Browser'})
    connection = urllib.request.urlopen(request)
    user_favourite_response_raw = connection.read()
    user_favourites[id] = json.loads(user_favourite_response_raw.decode('utf8'));
    print("Beginning loop through user list to find anime with id: " + id)
    for user_animeinfo in user_response["user_list_response"]["myanimelist"]["anime"]:
      if(user_animeinfo["series_animedb_id"] == id):
        user_favourites[id]["user_score"] = user_animeinfo["my_score"]


  jobs = [gevent.spawn(favouriteToArray, animeid) for animeid in user_response["user_profile_response"]["favourites"]["anime"]]

  gevent.joinall(jobs) # call all gvents

  favourite_arr = [] # Will fill up with markdown
  for key, favourite in user_favourites.items():
    favourite_arr.append(
      favourite["type"] + """ | """ + str('{0:.2f}'.format(favourite["score"])) + """ | """ + str('{0:.2f}'.format(int(favourite["user_score"]))) + """ | [""" + favourite["title"] + """](""" + favourite["url"] + """) \n"""
    )

  if(len(favourite_arr) == 0):
    favourite_str = "*None* | *None* | *None*"
  else:
    favourite_str = ''.join(favourite_arr)




  # submit(title, selftext=None, url=None resubmit=True, send_replies=True)
  # edit(body)
  post.edit("""#Here is today's overview of MyAnimeList!
^^Generated automatically by MAL-bot at ^^""" + d.strftime('%Y-%m-%d') + """

---
## Top 5 ranking anime
Rank | MAL Score | Title
:--:|:--:|:--
""" +
str(anime_top_response["items"][0]["rank"]) + """ | """ + str('{0:.2f}'.format(anime_top_response["items"][0]["score"])) + """ | [""" + anime_top_response["items"][0]["title"] + """](""" + anime_top_response["items"][0]["url"] + """) \n""" +
str(anime_top_response["items"][1]["rank"]) + """ | """ + str('{0:.2f}'.format(anime_top_response["items"][1]["score"])) + """ | [""" + anime_top_response["items"][1]["title"] + """](""" + anime_top_response["items"][1]["url"] + """) \n""" +
str(anime_top_response["items"][2]["rank"]) + """ | """ + str('{0:.2f}'.format(anime_top_response["items"][2]["score"])) + """ | [""" + anime_top_response["items"][2]["title"] + """](""" + anime_top_response["items"][2]["url"] + """) \n""" +
str(anime_top_response["items"][3]["rank"]) + """ | """ + str('{0:.2f}'.format(anime_top_response["items"][3]["score"])) + """ | [""" + anime_top_response["items"][3]["title"] + """](""" + anime_top_response["items"][3]["url"] + """) \n""" +
str(anime_top_response["items"][4]["rank"]) + """ | """ + str('{0:.2f}'.format(anime_top_response["items"][4]["score"])) + """ | [""" + anime_top_response["items"][4]["title"] + """](""" + anime_top_response["items"][4]["url"] + """) \n""" + """

---
## 5 Random anime
Type | MAL Score | Title
:--|:--:|:--
""" +
anime_random1_response["type"]  + """ | """ + str('{0:.2f}'.format(anime_random1_response["score"])) + """ | [""" + anime_random1_response["title"] + """](""" + anime_random1_response["url"] + """) \n""" +
anime_random2_response["type"]  + """ | """ + str('{0:.2f}'.format(anime_random2_response["score"])) + """ | [""" + anime_random2_response["title"] + """](""" + anime_random2_response["url"] + """) \n""" +
anime_random3_response["type"]  + """ | """ + str('{0:.2f}'.format(anime_random3_response["score"])) + """ | [""" + anime_random3_response["title"] + """](""" + anime_random3_response["url"] + """) \n""" +
anime_random4_response["type"]  + """ | """ + str('{0:.2f}'.format(anime_random4_response["score"])) + """ | [""" + anime_random4_response["title"] + """](""" + anime_random4_response["url"] + """) \n""" +
anime_random5_response["type"]  + """ | """ + str('{0:.2f}'.format(anime_random5_response["score"])) + """ | [""" + anime_random5_response["title"] + """](""" + anime_random5_response["url"] + """) \n""" + """

---
Today's random user is... """ + chosen_mal_username + """!
## [""" + chosen_mal_username + """](https://myanimelist.net/profile/""" + chosen_mal_username + """)'s favourite anime
Type | MAL Score | """ + chosen_mal_username + """'s Score | Title
:--|:--:|:--:|:--
""" + favourite_str)
  print("Done.")

# def end


scheduler = BlockingScheduler()

scheduler.add_job(scheduled_job, 'interval', minutes=2)
scheduler.start()