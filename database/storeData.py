import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate('/content/cc-recomendation-firebase-adminsdk-xe1r9-d36ef51293.json')

#Will have to uncomment this the first time running the code
# firebase_admin.initialize_app(cred, {
#   'databaseURL': 'https://cc-recomendation-default-rtdb.firebaseio.com/'
# })

database_dict = fully_labeled_data.set_index('Credit Card').to_dict(orient='index')

for card, data in database_dict.items():
  ref = db.reference(f'{card}')
  ref.set(data)