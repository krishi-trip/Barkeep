import pandas as pd
import numpy as np

struct = ["Card_Name", "Annual Fee", "Credit Line", "Credit Score", "Dining", "Entertainment", "Kudos", "Sentiment", "Travel"]

# data rows
data = [
    ['Burgundy Bichon Frise','1','137'],
    ['Pumpkin Pomeranian','1','182'],
    ['Purple Puffin','1','125'],
    ['Wisteria Wombat','1','109'],
    ['Burgundy Bichon Frise','2','168'],
    ['Pumpkin Pomeranian','2','141'],
    ['Purple Puffin','2','143'],
    ['Wisteria Wombat','2','167'],
    ['Burgundy Bichon Frise','3','154'],
    ['Pumpkin Pomeranian','3','175'],
    ['Purple Puffin','3','128'],
    ['Wisteria Wombat','3','167']]
df = pd.DataFrame(data, columns=['animal', 'region', 'n'])

df.region = pd.to_numeric(df.region)
df.n = pd.to_numeric(df.n)

z = df[['animal', 'n']].groupby(('animal')).mean()
print(z)

z.to_csv('CardData.csv')