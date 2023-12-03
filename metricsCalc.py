import pandas as pd
import numpy as np

df = pd.read_csv("CardData.csv")

cc_columns = ['Credit Card', 'Travel Rewards', 'Entertainment Rewards', 'Dining Rewards', 'Gas Rewards', 'Grocery Rewards', 'Annual Fee', 'Credit Line', 'Credit Score']
df.columns = cc_columns

num_of_results = 10

user_credit_score = int(input("What is your credit score?\n"))
if (user_credit_score < 350 or user_credit_score > 850):
    print("Invalid Credit Score")
    exit()
    
# parameters = ["Travel Rewards", "Dining Rewards"]
param = []

for b in range(len(cc_columns)-2):
    c = b+1
    i = 0
    while i == 0:
        try:
            val = int(input("Is " + str(cc_columns[c]) + " important to you? (0 for no, 1 for yes)\n"))
            if val != 0 and val != 1:
                raise Exception("Must be 0 or 1")
            if (val == 1):
                param.append(cc_columns[c])
            i = 1
        except:
            print("Must be a 0 or 1")

if (len(param) == 0):
    print("Since nothing was selected, selecting best overall card")
    param = cc_columns[1:]


df['Fit'] = df[param].sum(axis=1)


# Filters the Cards that don't meet the user's credit card score
fil = df.loc[df['Credit Score'] < user_credit_score]

# Sorts by the Fit value we calculated
fil = fil.sort_values('Fit', ascending=False)

# Selects the first x results
fil = fil.head(num_of_results)

# Selects the two columns we are interested at the end
fil = fil[['Credit Card']]

if num_of_results > fil.shape[0]:
    num_of_results = fil.shape[0]

print("Here are the best " + str(num_of_results) + " cards for you!")
print(fil.to_string(index=False))