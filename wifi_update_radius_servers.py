import csv
import meraki
import random

# Add your network IDs to a CSV file and change the 
# location to said file here
networks = []
with open('./assets/network_ids.csv', encoding="UTF-8") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    networks = [row[0] for row in reader]

# Add your Meraki API key here
dashboard = meraki.DashboardAPI('meraki_api_key')

# Define the radius servers
radius_servers = [
    {
        'host': 'first.ip.address.of.radius.server',
        'port': 1812,
        'secret': 'secretsecretsecret',
    },
    {
        'host': 'second.ip.address.of.radius.server',
        'port': 1812,
        'secret': 'secretsecretsecret',
    },
    {
        'host': 'third.ip.address.of.radius.server',
        'port': 1812,
        'secret': 'secretsecretsecret',
    },
]

# Get the SSID numbers for SSIDs that need updating
# Remove or add an elif if you need to edit more or less
# than 3 SSIDs
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

    # Shuffle the radius_servers list randomly
    random.shuffle(radius_servers)
    print(radius_servers)

    # Update the SSIDs for ssid_1
    try:
        ssid = dashboard.wireless.getNetworkWirelessSsid(network, ssid_1_number)
        ssid['authMode'] = '8021x-radius'
        ssid['encryptionMode'] = 'wpa'  # Update the encryption mode
        ssid['radiusFailoverPolicy'] = 'Deny access'  # Set the failover policy
        ssid['radiusLoadBalancingPolicy'] = 'Round robin' # Sets the load balancing policy
        ssid['radiusServers'] = radius_servers
        ssid_data = {key: ssid[key] for key in ssid if key not in ['number', 'wpa-eap']}  # Exclude 'number' and 'wpa-eap' keys
        dashboard.wireless.updateNetworkWirelessSsid(networkId=network, number=ssid_1_number, **ssid_data)
    except Exception as e:
        print('Error updating ssid_1 SSID:', e)

    # Update the SSIDs for ssid_2
    try:
        ssid = dashboard.wireless.getNetworkWirelessSsid(network, ssid_2_number)
        ssid['authMode'] = '8021x-radius'
        ssid['encryptionMode'] = 'wpa'  # Update the encryption mode
        ssid['radiusFailoverPolicy'] = 'Deny access'  # Set the failover policy
        ssid['radiusLoadBalancingPolicy'] = 'Round robin' # Sets the load balancing policy
        ssid['radiusServers'] = radius_servers
        ssid_data = {key: ssid[key] for key in ssid if key not in ['number', 'wpa-eap']}  # Exclude 'number' and 'wpa-eap' keys
        dashboard.wireless.updateNetworkWirelessSsid(networkId=network, number=ssid_2_number, **ssid_data)
    except Exception as e:
        print('Error updating ssid_2 SSID:', e)

    # Update the SSIDs for ssid_3
    try:
        ssid = dashboard.wireless.getNetworkWirelessSsid(network, ssid_3_number)
        ssid['authMode'] = '8021x-radius'
        ssid['encryptionMode'] = 'wpa'  # Update the encryption mode
        ssid['radiusFailoverPolicy'] = 'Deny access'  # Set the failover policy
        ssid['radiusLoadBalancingPolicy'] = 'Round robin' # Sets the load balancing policy
        ssid['radiusServers'] = radius_servers
        ssid_data = {key: ssid[key] for key in ssid if key not in ['number', 'wpa-eap']}  # Exclude 'number' and 'wpa-eap' keys
        dashboard.wireless.updateNetworkWirelessSsid(networkId=network, number=ssid_3_number, **ssid_data)
    except Exception as e:
        print('Error updating ssid_3 SSID:', e)
