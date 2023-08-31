""" Python Script to Update Walled Garden URLs for SSID1  """
import csv
import time
import requests

# API Key
API_KEY = "meraki_api_key"

# Meraki API URL
BASE_URL = "https://api.meraki.com/api/v1"

# Define the SSID name to update
SSID_NAME = "SSID1"

# Pulls network_ids from a CSV file.
NETWORK_IDS = []
with open("./assets/network_ids.csv", encoding="UTF-8") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        NETWORK_IDS.append(row[0])

# Pulls walled garden URLs from a CSV file.
WG_URLS = []
with open("./assets/walled_garden_urls.csv", encoding="UTF-8") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        WG_URLS.append(row[0])

# Iterate through the list of network IDs
for network_id in NETWORK_IDS:

    # Get a list of SSIDs for the network
    response = requests.get(f"{BASE_URL}/networks/{network_id}"
                                   "/wireless/ssids",
                                   headers={"X-Cisco-Meraki-API-Key": API_KEY})
    ssids = response.json()

    # Find the SSID with the given name
    SSID_ID = None
    for ssid in ssids:
        if ssid['name'] == SSID_NAME:
            SSID_ID = ssid['number']

    # If the SSID was found, update the walled garden ranges
    if SSID_ID:
        update_url = f"{BASE_URL}/networks/{network_id}/wireless/ssids/{SSID_ID}"
        payload = {
            "walledGardenEnabled": True,
            "walledGardenRanges": WG_URLS
        }

    # Update the walled garden settings for the network
    update_response = requests.put(update_url,
                                       headers={"X-Cisco-Meraki-API-Key": API_KEY},
                                       json=payload)

    if update_response.status_code == 200:
        print(f"Walled Garden updated for network ID: {network_id}")
    elif update_response.status_code == 429:
        time.sleep(int(update_response.headers["Retry-After"]))
    else:
        print(f"Walled Garden update failed for network ID: \
              {network_id}. Error code: {update_response.status_code}")
