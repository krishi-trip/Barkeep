#!/bin/bash
echo "Checking for Requirements"
pip install -r requirements.txt

echo "Executing Pipeline"

echo "Running webscrapper"
python database/webScraper.py

echo "Parsing data with GPT"
python model/getGptLabeling.py

echo "Calculating metrics"
python model/calculateMetrics.py

echo "Update chatbot metrics"
cp CardData.csv chatbot/CardData.csv
# How often does AWS update?

echo "Update databse"
python database/storeData.py

echo "Finished Pipeline"
