import pandas as pd
import re
import random
# from nltk.sentiment import SentimentIntensityAnalyzer

# Sample DataFrame with posts
data = {
    'Post_ID': [1, 2, 3, 4, 5],
    'Post_Content': ["Content 1", "Content 2", "Content 3", "Content 4", "Content 5"],
}

df = pd.DataFrame(data)

# List of credit card types for matching (you can extend this list)
credit_card_types = ['Visa', 'Mastercard', 'American Express', 'Discover', 'Credit Card']
    
def get_credit_card_type(post_content):
    # Regular expression pattern for case-insensitive matching
    pattern = re.compile('|'.join(credit_card_types), re.IGNORECASE)

    # Check if the post content contains any credit card type
    return bool(re.search(pattern, post_content))

def get_user_sentiment(post_content):
    # Initialize the SentimentIntensityAnalyzer
    # sid = SentimentIntensityAnalyzer()

    # Get the sentiment polarity score
    # sentiment_score = sid.polarity_scores(post_content)
    sentiment_score = random.randint(-2, 2)

    # Determine sentiment based on the compound score
    if sentiment_score >= 0.05:
        return 'Positive'
    elif sentiment_score <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

# Function to label posts with Credit Card Type
def label_credit_card_type(post):
    # Add your logic to determine the credit card type based on post content
    # For simplicity, let's assume you have a function get_credit_card_type() for this purpose
    return get_credit_card_type(post['Post_Content'])

# Function to label posts with User Sentiment
def label_user_sentiment(post):
    # Add your logic to determine user sentiment based on post content
    # For simplicity, let's assume you have a function get_user_sentiment() for this purpose
    return get_user_sentiment(post['Post_Content'])

# Apply label functions to DataFrame
df['Credit_Card_Type'] = df.apply(label_credit_card_type, axis=1)
df['User_Sentiment'] = df.apply(label_user_sentiment, axis=1)

# Display the labeled DataFrame
print(df)
