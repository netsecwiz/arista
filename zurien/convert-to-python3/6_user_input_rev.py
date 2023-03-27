#!/usr/bin/python3

import requests
import json
import os
import sys
import getpass

# Disable SSL warnings and verification (not recommended for production use)
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
verify_ssl = False

u = input('Enter Username: ')
p = getpass.getpass('Enter Password: ')

a = 1
b = 5

def allsw():
    for x in range(a, b):
        host = f'leaf{x}'
        conn = os.system(f"ping -c 1 {host} > /dev/null")

        if conn == 0:
            url = f'https://{u}:{p}@{host}/command-api'
            payload = {
                'jsonrpc': '2.0',
                'method': 'runCmds',
                'params': {
                    'format': 'json',
                    'timestamps': False,
                    'autoComplete': False,
                    'expandAliases': False,
                    'cmds': ['show hostname'],
                    'version': 1
                },
                'id': 'EapiExplorer-1'
            }

            response = requests.post(url, json=payload, auth=(u, p), verify=verify_ssl)

            if response.status_code == 200:
                hostname = response.json()['result'][0]['hostname']
                print(f'{hostname} {host} is reachable')
            else:
                print(f'Switch {host} is unreachable due to error: {response.status_code} - {response.text}')
        else:
            print(f'Switch {host} is unreachable')


allsw()
