import sys
import os
import pandas as pd
import re
import random
import requests
import json
from bs4 import BeautifulSoup


#URL of the FicoForums website
BASE_URL = 'https://ficoforums.myfico.com/'
#URL of the credit card forums
FORUM_URL = 'https://ficoforums.myfico.com/t5/Credit-Cards/bd-p/creditcard'
# A common user agent, can help bypass some scraping restrictions
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

#Parameters
f = open(os.path.dirname(__file__) + "/../parameters.json")
param = json.load(f)
target_pages = param['targetPages']
min_kudos = param['minKudos']
debug_mode = param['debugMode']
f.close()

#Making sure we get at least 1 page of posts
if target_pages <= 0:
  target_pages = 1
  
#Function that gets the title and linkss of each post
def get_post_links_and_titles(url):
  #List that has all the post details
  post_list = []

  #For every page in the credit card forums (1, 4384)
  for i in range(1, target_pages+1):
    #If it is the first page, keep the URL as is
    if i == 1:
      response = requests.get(url, headers=headers)

    #If if is any other page, append the page number to the URL
    else:
      new_URL = "{}/page/{}".format(url, i)
      response = requests.get(new_URL, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')
    #Finds all of the posts on the page
    posts = soup.find_all('h2', class_='message-subject')

    for post in posts:
      #Gets the link of the post
      link_tag = post.find('a', class_='page-link')
      title = link_tag.text.strip()
      link = BASE_URL + link_tag['href']
      post_list.append({
          'title': title,
          'link': link
      })

  return post_list

post_list = get_post_links_and_titles(FORUM_URL)
#Removing the first 4 links which are info/help thread posts
post_list = post_list[4:]

if debug_mode == 1:
  for post in range(len(post_list)):
    print(post_list[post]['link'])

#Function that gets the contents and replies of each post
def get_post_data_and_kudos(post_list):
  post_content = []

  for post in post_list:
    url = post['link']

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    #Get the title of the post
    title = soup.find_all('div', class_='lia-message-subject')
    #Get the post and all its replies
    content = soup.find_all('div', class_='lia-message-body-content')
    #Get the Kudos of the post and all its replies
    kudos = soup.find_all('span', class_='MessageKudosCount')

    #Get the post kudos
    main_post_kudos = int(kudos[0].text.strip())

    #Filter the post based on Kudos
    if (main_post_kudos < min_kudos):
      continue

    #Separate the post
    main_post = content[0].text.strip()
    #Separate the replies
    post_replies = content[1:]

    replies = []

    #Add all of the replies and their Kudos to a list
    for i in range(len(post_replies)):
      reply_kudos = int(kudos[i].text.strip())

      #Filter the reply based on Kudos
      if (reply_kudos < min_kudos):
        continue

      #Add the reply to the list
      replies.append({
          'Reply': post_replies[i].text.strip(),
          'Kudos': reply_kudos
      })

    #Add the post and its replies to the list of posts
    post_content.append({
        'Title': title[0].text.strip(),
        'Message': main_post,
        'Kudos': main_post_kudos,
        'Replies': replies
    })

  return post_content

post_content = get_post_data_and_kudos(post_list)
with open(os.path.dirname(__file__) + '/../data.json', 'w') as f:
    json.dump(post_content, f)

if debug_mode == 1:
  for post in post_content:
    print(f"Message: {post['Message']}\nKudos: {post['Kudos']}")
    for reply in range(len(post['Replies'])):
      print(f"Reply: {post['Replies'][reply]['Reply']}\nKudos: {post['Replies'][reply]['Kudos']}")
    print(f"{'-'*250}")
  print(len(post_content))
