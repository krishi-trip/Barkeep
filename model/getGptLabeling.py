import openai
import json
import os.path
import pandas as pd
from tqdm import tqdm

pbar = tqdm(total=100)
post_content = []
with open(os.path.dirname(__file__) + '/../data.json') as json_file:
    post_content = json.load(json_file)

API_KEY = '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'
openai.api_key = API_KEY
model_id = 'gpt-3.5-turbo-1106'

prompt = """
The above text is a post from myFICO, under a credit card forum, where people can post about
their credit card questions or tips or just generally stay updated on credit cards.
In addition to the article the replies have been added, which should help give you more information
about the context of the article.

Read the article and all of its replies and identify all credit cards that are talked about. For each credit card,
score the following categories:

    Travel Rewards (Cash Back)

    Entertainment Rewards (Cash Back)

    Dining Rewards (Cash Back)

    Gas Rewards (Cash Back)

    Grocery Rewards (Cash Back)

    Annual Fee

    Credit Line

    Credit Score

For each aspect (except Credit Score):
Rate a category 1 if the article describes that aspect of the credit card to be positive, or if you know it to be positive.
Rate a category -1 if the article describes that aspect of the credit card to be negative, or if you know it to be negative.
Rate a category 0 if you are not sure.

Give the Credit Score category a value that matches the Credit Score of the card if stated in the above text, else give the category -1.

Finally, output your ratings with the following format:

Credit Card name: "Name of Card"
Travel Rewards: 1
Entertainment Rewards: 1
Dining Rewards: 0
Gas Rewards: -1
Grocery Rewards: 0
Annual Fee: 0
Credit Line: 1
Credit Score: 650

Only output the above, provide 0 explanation or any other additional text. Only the data.
"""

#Function that takes in a query and returns the response from the gpt model
def get_gpt_response(user_query):
  conversation = [{'role': 'system'}]
  conversation[0]['content'] = user_query
  response = openai.chat.completions.create(
      model=model_id,
      messages=conversation
  )
  return response.choices[0].message.content

#Function that takes in the scraped data, queries the gpt model, and returns a list of labeled data
def get_labeled_data(post_content):
  labeled_data = []

  for post in post_content:
    orig_post = post['Message']
    replies = ""
    for reply in range(len(post['Replies'])):
      replies = replies + post['Replies'][reply]['Reply']

    #Querying the gpt model with one post with all its replies
    gpt_response = get_gpt_response(prompt  + orig_post + replies)
    labeled_data.append(gpt_response)
    updateVal = 33 / len(post_content)
    pbar.update(updateVal)

  return labeled_data

#Getting all the gpt labeled data
raw_labeled_data = get_labeled_data(post_content)


#Function to split up multiple credit cards in the same gpt respsonse
def split_responses(responses):
  return [response.strip() for response in responses.split("\n\n")]

#Function to get rid of all invalid characters in the labeled data
def remove_quotes(response):
  return response.replace('"','').replace('.','').replace('#','').replace('NaN','-1').replace('None','-1').replace('nan','-1')

#Function to get rid of invalid gpt responses
def is_valid_response(response):
  return all(':' in line for line in response.split('\n'))


def make_responses_valid(responses):
  split_data = []

  #Making sure that each entry in the array is a single response
  for response in responses:
    split_data.extend(split_responses(response))
    updateVal = 33 / len(responses)
    pbar.update(updateVal)

  #Removing all invalid characters from the response
  valid_char_data = [remove_quotes(response) for response in split_data]

  #Removes responses that dont have semi-colons
  valid_data = [response for response in valid_char_data if is_valid_response(response)]

  return [response for response in valid_data if "**" not in response]

filtered_labeled_data = make_responses_valid(raw_labeled_data)

#Function to turn the labeled data into a dataframe of all the credit cards
def collectivize_data(data):
  df = pd.DataFrame(data, columns=['Credit Card', 'Travel Rewards', 'Entertainment Rewards', 'Dining Rewards', 'Gas Rewards', 'Grocery Rewards', 'Annual Fee', 'Credit Line', 'Credit Score'])

  numeric_columns = ['Travel Rewards', 'Entertainment Rewards', 'Dining Rewards', 'Gas Rewards', 'Grocery Rewards', 'Annual Fee', 'Credit Line', 'Credit Score']
  df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')
  collectivized_df = df.groupby('Credit Card').mean().reset_index()
  return collectivized_df.fillna(-1)

#Function to convert the gpt response to numbers
def process_labeled_data(data):
  processed_data = []

  for credit_card in data:
    if not credit_card:
      continue

    labeled_cc = credit_card.splitlines()
    cc_data = []
    for i in range(len(labeled_cc)):

      key, value = [item.strip() for item in labeled_cc[i].split(':')]
      try:
        cc_data.append(int(value))
      except ValueError:
        cc_data.append(value)

    processed_data.append(cc_data)
    
    updateVal = 33 / len(data)
    pbar.update(updateVal)

  return collectivize_data(processed_data)

fully_labeled_data = process_labeled_data(filtered_labeled_data).round(3)
fully_labeled_data.to_csv('CardData.csv', index=False)
pbar.close()
