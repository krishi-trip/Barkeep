import openai
# import pandas as pd 
# import numpy as np 

API_KEY = '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'
openai.api_key = API_KEY
model_id = 'gpt-3.5-turbo'

prompt = """
The above article is an article from myFICO, a website where people can post about their financial issues or
just generally stay updated about anything related to finance. In addition to the article the replies have been 
added, which should help give you more information about the context of the article. 

Read the article and all of its replies and identify all credit cards that are talked about. For each credit card,
score the following categories:

    Travel Rewards (Cash Back)

    Entertainment Rewards (Cash Back)

    Dining Rewards (Cash Back)

    Annual Fee

    Credit Line

    Credit Score

Rate a category 1 if the article describes that aspect of the credit card to be positive, or if you know it to be positive. 
Rate a category -1 if the article describes that aspect of the credit card to be negative, or if you know it to be negative.
Rate a category 0 if you are not sure. 

Finally, output your ratings with the following format:

Credit Card name: -1
Travel Rewards: 1
Entertainment Rewards: 1
Dining Rewards: 0
Annual Fee: -1
Credit Line: 1
Credit Score: 1

Only output the above, provide 0 explanation or any other additional text. Only the data.
"""



def get_gpt_response(user_query):
    conversation = [{'role': 'system'}]
    conversation[0]['content'] = user_query
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=conversation
    )
    return response['choices'][0]['message']['content']

print(get_gpt_response(prompt))

# ratings = pd.DataFrame()

# for i in range(num_articles): 
    # updated_prompt = data_file[i] + '\n' + prompt
    # rating = get_gpt_response(updated_prompt)
    # ratings.append(rating)

