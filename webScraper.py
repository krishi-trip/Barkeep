import requests
from bs4 import BeautifulSoup

#URL of the FicoForums website
BASE_URL = 'https://ficoforums.myfico.com/'

#URL of the credit card forums
FORUM_URL = 'https://ficoforums.myfico.com/t5/Credit-Cards/bd-p/creditcard'

# A common user agent, can help bypass some scraping restrictions
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

#print("{}/page/{}".format(FORUM_URL, 2))

def get_post_links_and_titles(url):
  #List that has all the post details
  post_list = []

  #For every page in the credit card forums (1, 4384)
  for i in range(1, 2):
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
print(post_list[0]['link'])

def get_post_data_and_kudos(post_list):
  post_details = []

  for post in post_list:
    url = post['link']

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    details = soup.find_all('div', class_='lia-message-body-content')
    kudos = soup.find_all('span', class_='MessageKudosCount')

    for i in range(len(details)):
      post_kudos = int(kudos[i].text.strip())
      post_text = details[i].text.strip()
      post_details.append({
          'Message': post_text,
          'Kudos': post_kudos
      })

    return post_details

post_details = get_post_data_and_kudos(post_list)
