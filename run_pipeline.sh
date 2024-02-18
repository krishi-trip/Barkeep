#!/bin/bash

echo "Checking for Requirements"
pip install -r requirements.txt | grep -v 'already satisfied\|Defaulting to user installation'

echo "Executing Pipeline"

echo "Running webscrapper"
python webScraper.py

echo "Parsing data with GPT"
python getGptLabeling.py

echo "Update chatbot metrics"
cp CardData.csv chatbot/CardData.csv
# How often does AWS update?

echo "Finished Pipeline"
