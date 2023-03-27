#!/usr/bin/python3

import requests
import json
import os
import sys
import getpass
from usrvar import *
from swvar import *

# Disable SSL warnings and verification (not recommended for production use)
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
verify_ssl = False

inam = input('Interface Name: ')

def allsw():

    for x in range(a, b):
        host = net + str(x)
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
                    'cmds': [
                        {'cmd': 'enable', 'input': en},
                        'configure',
                        f'no interface {inam}',
                        'show hostname',
                    ],
                    'version': 1
                },
                'id': 'EapiExplorer-1'
            }

            response = requests.post(url, json=payload, auth=(u, p), verify=verify_ssl)

            if response.status_code == 200:
                try:
                    hostname = response.json()['result'][3]['hostname']
                except KeyError:
                    print(f"Hostname not found in the response for {host}. Response: {response.json()}")
                    continue
                print(f'{hostname} - {inam} is deleted')
            else:
                print(f'Switch {host} is unreachable due to error: {response.status_code} - {response.text}')
        else:
            print(f'Switch {host} is unreachable')


allsw()
