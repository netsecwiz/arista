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

# Prepare the JSON-RPC payload
payload = {
    'jsonrpc': '2.0',
    'method': 'runCmds',
    'params': {
        'format': 'text',
        'timestamps': False,
        'autoComplete': False,
        'expandAliases': False,
        'cmds': [
            'enable',
            'show running-config'
        ],
        'version': 1
    },
    'id': 'EapiExplorer-1'
}

# Send the JSON-RPC request
response = requests.post(url, json=payload, auth=(username, password), verify=verify_ssl)

# Check if the request was successful
if response.status_code == 200:
    result = response.json()['result']
    print(result[1]["output"])
else:
    print(f'Error: {response.status_code} - {response.text}')