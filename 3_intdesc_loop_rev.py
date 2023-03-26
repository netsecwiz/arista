#!/usr/bin/python3

import requests
import json

# Replace with your switch's username, password, and IP address
username = 'spoonman'
password = 'arista'
switch_ip = 'leaf1'

url = f'https://{switch_ip}/command-api'

# Disable SSL warnings and verification (not recommended for production use)
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
verify_ssl = False

for x in range(1, 11):
    # Prepare the JSON-RPC payload
    payload = {
        'jsonrpc': '2.0',
        'method': 'runCmds',
        'params': {
            'format': 'json',
            'timestamps': False,
            'autoComplete': False,
            'expandAliases': False,
            'cmds': [
                'enable',
                'configure',
                f'interface ethernet{x}',
                f'description Test Desc on Eth-{x}'
            ],
            'version': 1
        },
        'id': 'EapiExplorer-1'
    }

    # Send the JSON-RPC request
    response = requests.post(url, json=payload, auth=(username, password), verify=verify_ssl)

    # Check if the request was successful
    if response.status_code == 200:
        print(f"Interface Eth-{x} configured successfully.")
    else:
        print(f'Error configuring interface Eth-{x}: {response.status_code} - {response.text}')

print("Done.")
