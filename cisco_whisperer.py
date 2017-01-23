# -*- coding: utf-8 -*-
import paramiko
import requests
import json
import time
import datetime
from netmiko import ConnectHandler


def compare(x, y):
    a = datetime.datetime.strptime(x['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
    b = datetime.datetime.strptime(y['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
    c = int((a - b).total_seconds() * 100)
    return c


lastupdate = datetime.datetime.strptime('1970-01-01T00:00:00.000Z', '%Y-%m-%dT%H:%M:%S.%fZ')
while True:
    time.sleep(5)
    entries = json.loads(requests.get('https://somesite.com/installations').content)#this address was intentionally changed for security reasons
    entries = sorted(entries, cmp=compare)
    config = []
    for entry in entries:
        if datetime.datetime.strptime(entry['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ') > lastupdate:
            lastupdate = datetime.datetime.strptime(entry['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
            config.append(
                'ip route vrf Juwoto ' + entry['address'] + ' ' + entry['mask'] + ' ' + entry['framed_address'] + '\n')
    if config != []:
        host = '172.31.66.252'
        user = 'juwotouser'
        secret = 'uXp8KBJi2D0l'
        device = ConnectHandler(device_type='cisco_ios', ip=host, username=user, password=secret)
        print device.send_config_set(config)
