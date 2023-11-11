from django.shortcuts import render
from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def chatbot_page(request):
    return render(request, 'chatbot.html')

from django.http import JsonResponse

# This is a mockup database of cards and their primary features
cards_db = [
    {'name': 'Traveler Elite', 'type': 'Travel', 'monthly_fee': 0, 'benefit': '5x travel points'},
    {'name': 'DineMaster Gold', 'type': 'Dining', 'monthly_fee': 0, 'benefit': '10% cashback on dining'},
    {'name': 'CashSaver Platinum', 'type': 'Cashback', 'monthly_fee': 10, 'benefit': '5% cashback on all purchases'},
    # ... add other cards
]

def recommend_card(preferences):
    # Here you can implement a logic to recommend a card from the database based on the user preferences
    # This is a simple lookup by 'type' for the sake of example
    for card in cards_db:
        if card['type'] == preferences['type']:
            return card
    return None

def chatbot_response(request):
    user_message = request.GET.get('message', '').lower().strip()



    # Depending on the user's response, guide them through the conversation flow
    if 'hello, can you help me find the right credit card to get?' in user_message:
        response = "Hello! I can help you find the best credit card based on your preferences. May I ask you a few questions?"
    elif 'yes, you can ask me a few questions' in user_message.lower():
        response = "What are you planning on using this credit card for? (Options include dining, travel, cash-back, etc.)"
    elif 'the main purpose of my credit card will be for travel.' in user_message:
        response = "Great choice! What's your estimated monthly spending on travel?"
        # Save the preference somewhere, for this example we are just moving forward
    elif 'i will spend around $1000 on travel.' in user_message:  # Check if the user entered a number for monthly spending
        response = "do you prefer no annual fees?"
    elif 'no, i dont want any annual fees for the credit card.' in user_message:
        card = recommend_card({'type': 'Travel'})  # Mockup: Here, we are just fetching a travel card
        response = f"Based on your preferences and analysis of data from the MyFico Forums website, the {card['name']} credit card might be a great fit for you. It offers {card['benefit']}. The credit card has no annual fees, and it will fit your traveling budget."
    else:
        response = "I'm not sure about that. Can you please specify your preference or ask another question?"

    return JsonResponse({'response': response})


