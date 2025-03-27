import json
import random

# Load the website list from website_list.json
with open("../website_list.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Shuffle the websites list
random.shuffle(data["websites"])

# Save the shuffled list to demo2.json
with open("../website_list_final.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=2, ensure_ascii=False)

print("Shuffled website list saved to demo.json")