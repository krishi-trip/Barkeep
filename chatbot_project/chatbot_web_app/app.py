from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

df = pd.read_csv("CardData.csv")
cc_columns = ['Credit Card', 'Travel Rewards', 'Entertainment Rewards', 'Dining Rewards', 'Gas Rewards', 'Grocery Rewards', 'Annual Fee', 'Credit Line', 'Credit Score']
df.columns = cc_columns

question_index = 0
user_responses = {}
param = []
num_of_results = 10
user_credit_score = None

questions = ["What is your credit score?"] + [f"Is {cc} important to you? (0 for no, 1 for yes)" for cc in cc_columns[1:-2]]

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    global question_index, user_responses, param, user_credit_score, df

    user_input = request.form["msg"]

    if user_input.lower() in ['hi', 'hello', 'start']:
        question_index = 0
        user_responses.clear()
        param = []
        user_credit_score = None
        return "Hello! I am your credit card recommendation assistant. " + questions[question_index]

    if question_index == 0:
        try:
            user_credit_score = int(user_input)
            if user_credit_score < 350 or user_credit_score > 850:
                return "Invalid Credit Score. Please enter a valid credit score."
            question_index += 1
            return questions[question_index]
        except ValueError:
            return "Please enter a valid integer for your credit score."

    elif question_index < len(questions):
        try:
            val = int(user_input)
            if val not in [0, 1]:
                return "Must be a 0 or 1. " + questions[question_index]
            if val == 1:
                param.append(cc_columns[question_index - 1])
            question_index += 1
        except ValueError:
            return "Must be a 0 or 1. " + questions[question_index]

        if question_index < len(questions):
            return questions[question_index]
        else:
            return compute_recommendations()

    return "I'm not sure how to respond to that. Could you please rephrase?"

def compute_recommendations():
    global df, param, user_credit_score, num_of_results

    valid_params = [p for p in param if p in df.columns]
    if not valid_params:
        valid_params = cc_columns[1:-2]  

    df['Fit'] = df[valid_params].sum(axis=1)
    fil = df.loc[df['Credit Score'] <= user_credit_score]
    fil = fil.sort_values('Fit', ascending=False)
    fil = fil.head(num_of_results)
    fil = fil[['Credit Card']]

    if num_of_results > fil.shape[0]:
        num_of_results = fil.shape[0]

    formatted_output = "\n".join(f"{i+1}. {card}" for i, card in enumerate(fil['Credit Card']))
    return f"Here are the best {num_of_results} cards for you:\n{formatted_output}"


if __name__ == '__main__':
    app.run()
