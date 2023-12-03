from flask import Flask, render_template, request, jsonify
from openai import OpenAI

client = OpenAI(api_key='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')

app = Flask(__name__)

questions = [
    "Are you interested in earning rewards for travel-related expenses like flights and hotels? If so, what percentage of cash back would you find appealing for these expenses?",
    "Would you like to earn cash back for entertainment expenses such as movie theaters, amusement parks, and tourist attractions? Please specify the cash back percentage you're looking for.",
    "Do you want to receive cash back on dining, including restaurants and cafes? If yes, indicate the desired cash back percentage.",
    "Are you willing to pay an annual fee for a credit card? If so, what is the maximum annual fee you would consider?", 
    "What is the ideal credit limit you would like on your credit card? This is the maximum amount you can borrow at any time.",
    "Could you provide your current credit score range? This information helps in recommending a card that matches your credit profile.",
]

question_index = 0

user_responses = {}

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    global question_index
    user_input = request.form["msg"]

    if user_input.lower() in ['hi', 'hello', 'start']:
        question_index = 0
        user_responses.clear()
        return "Hello! I am your credit card recommendation assistant. " + questions[question_index]

    if question_index < len(questions):
        user_responses[questions[question_index]] = user_input
        question_index += 1
        if question_index < len(questions):
            return questions[question_index]
        else:
            return process_responses_with_gpt()

    return "I'm not sure how to respond to that. Could you please rephrase?"

def process_responses_with_gpt():
    prompt = "Process and categorize user responses based on the following criteria:\n\n"
    prompt += "1. Travel Rewards (Cash Back):\n   - 0% : 0\n   - 1% : 1\n   - 2% : 2\n   - 3% : 3\n   - 4% : 4\n   - 5% : 5\n   - 6+% : 6\n\n"
    prompt += "2. Entertainment Rewards (Cash Back):\n   - [Same breakdown as Travel Rewards]\n\n"
    prompt += "3. Dining Rewards (Cash Back):\n   - [Same breakdown as Travel Rewards]\n\n"
    prompt += "4. Annual Fee:\n   - $0: 0\n   - $1 - $100: 1\n   - $101 - $200: 2\n   - $201 - $300: 3\n   - $301 - $400: 4\n   - $401 - $500: 5\n   - $500+: 6\n\n"
    prompt += "5. Credit Line:\n   - $0-$5,000: 1\n   - $5,001-$10,000: 2\n   - $10,001-$15,000: 3\n   - $15,001-$20,000: 4\n   - $20,001-$25,000: 5\n   - $25,001-$30,000: 6\n\n"
    prompt += "6. Credit Score:\n   - 300 - 579: 0\n   - 580 - 669: 1\n   - 670 - 739: 2\n   - 740 - 799: 3\n   - 800 - 850: 4\n\n"
    prompt += "Given the user responses:\n"
    for q, response in zip(questions, user_responses.values()):
        prompt += f"- {q}: {response}\n"
    prompt += "\nCategorize each response according to the sections above and format the output as a string in the following format: 'Travel: X, Entertainment: Y, Dining: Z, Annual Fee: A, Credit Line: B, Credit Score: C'."

    try:
        response = client.completions.create(
            model="gpt-3.5-turbo",
            prompt=prompt,
        )

        if isinstance(response, str):
            return response.strip()
        else:
            return response.choices[0].text.strip()

    except Exception as e:
        print(f"Error: {str(e)}")  
        return "There was an error processing your credit card recommendation."



if __name__ == '__main__':
    app.run()