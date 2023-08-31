# meraki
Python scripts to manage Meraki via API v1. Most scripts require the following:

- A csv file with a list of network ID as the first column. All other columns will be ignored, but not a bad idea to list the name of the network in the second column.

```
L_000000000000000001,Site1
L_000000000000000001,Site2
L_000000000000000001,Site3
```

## Content Filter Update Script

Used to update the allowed and blocked URLs along with blocked categories and threat categories. The following CSV files will be needed:

- allowed_urls.csv
- blocked_urls.csv
- blocked_categories.csv (contains both categories and threats)

Each CSV file expects the allowed/blocked URLS and categories in the first column. Categories should be in the format of:
```
meraki:contentFiltering/category/C7,Games
```
A list of categories and threats can be found here: https://talosintelligence.com/categories

(Note: Older MXs still use bright cloud and updating categories will not work with this script)

## Wifi Scripts
These scripts will update settings for APs only
### Radius Servers Updates
This script will update the RADIUS servers for SSID names that are specficied in the script starting on line 37
```
ssid_1_number = None
ssid_2_number = None
ssid_3_number = None
for network in networks:
    ssids = dashboard.wireless.getNetworkWirelessSsids(network)
    for ssid in ssids:
        if ssid['name'] == 'SSID1':
            ssid_1_number = ssid['number']
        elif ssid['name'] == 'SSID2':
            ssid_2_number = ssid['number']
        elif ssid['name'] == 'SSID3':
            ssid_3_number = ssid['number']
```
### Walled Garden Script
This script will update the walled garden if using a captive portal. Update the SSID_NAME variable with your walled garden enabled SSID and create a CSV file with the list of URLs that will be accessible prior to login.
