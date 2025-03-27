import json
from collections import Counter

# Load the website list from website_list.json
with open("../website_list_final.json", "r", encoding="utf-8") as file:
    data = json.load(file)

websites = data["websites"]

# Count occurrences
counter = Counter(websites)

# Find duplicates
duplicates = {url: count for url, count in counter.items() if count > 1}

# Print duplicates
if duplicates:
    print("Found duplicates:")
    for url, count in duplicates.items():
        print(f"{url} -> {count} times")
else:
    print("No duplicates found.")
