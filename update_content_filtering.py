""" Python Script to Update Meraki's Content Filtering """
import csv
import time
import requests

# API Key
API_KEY = "meraki_api_key"

# Meraki API URL
BASE_URL = "https://api.meraki.com/api/v1"

# Pulls network_ids from a CSV file.
network_ids = []
with open("./assets/network_ids.csv", encoding="UTF-8") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        network_ids.append(row[0])

# Pulls allowed URLs from a CSV file.
allowed_urls_set = set()
with open("./assets/allowed_urls.csv", encoding="UTF-8") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        allowed_urls_set.add(row[0])

# Pulls blocked URLs from a CSV file.
blocked_urls_set = []
with open("./assets/blocked_urls.csv", encoding="UTF-8") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        blocked_urls_set.append(row[0])

# List of categories to block from a CSV file.
blocked_categories = []
with open("./assets/blocked_categories.csv", encoding="UTF-8") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        blocked_categories.append(row[0])

# Iterate through the list of network IDs
for network_id in network_ids:

    # Get the current content filter settings for the network
    filter_response = requests.get(f"{BASE_URL}/networks/{network_id}"
                                   "/appliance/contentFiltering",
                                   headers={"X-Cisco-Meraki-API-Key": API_KEY})
    filter_settings = filter_response.json()

    # Gets current list of allowed_URLs
    allowed_urls = filter_settings.get("allowedUrlPatterns", [])

    # Add new entries to allowed URls list
    for url in allowed_urls_set:
        if url not in allowed_urls:
            allowed_urls.append(url)

    # Update the allowed URLs with the new list
    filter_settings["allowedUrlPatterns"] = allowed_urls

    # Gets current list of blocked URLs
    blocked_urls = filter_settings.get("blockedUrlPatterns", [])

    # Add new entries to blocked URls list
    for url in blocked_urls_set:
        if url not in blocked_urls:
            blocked_urls.append(url)

    # Update the blocked URLs with the new list
    filter_settings["blockedUrlPatterns"] = blocked_urls

    # Update the blocked categories with the new list
    filter_settings["blockedUrlCategories"] = blocked_categories

    # Update the content filter settings for the network
    update_response = requests.put(f"{BASE_URL}/networks/{network_id}"
                                   "/appliance/contentFiltering",
                                   headers={"X-Cisco-Meraki-API-Key": API_KEY},
                                   json=filter_settings)

    if update_response.status_code == 200:
        print(f"Content filter updated for network ID: {network_id}")
    elif update_response.status_code == 429:
        time.sleep(int(update_response.headers["Retry-After"]))
    else:
        print(f"Content filter update failed for network ID: \
              {network_id}. Error code: {update_response.status_code}")
