#!/bin/bash
echo "Checking for Requirements"
pip install -r requirements.txt

echo "Executing Pipeline"
python3 webScraper.py 1

# pass through model and relevant parts

echo "Finished Pipeline"
# echo where to see results or results themself