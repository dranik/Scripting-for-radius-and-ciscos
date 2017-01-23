 # -*- coding: utf-8 -*-
from subprocess import call
import requests
import json
import time
import hashlib


def hashfile(afile, hasher, blocksize=65536):
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    return hasher.digest()


hash_a = 'b'
while True:
    hash_b = hashfile(open('/etc/raddb/users', 'rb'), hashlib.md5())
    if hash_a != hash_b:
        hash_a = hash_b
        call(['systemctl','restart','radiusd'])
    time.sleep(5)
    try:
        text_file = open('/etc/raddb/users', 'w')
        entries = json.loads(requests.get('https://somesite.com/installations').content) #this address was intentionally changed for security reasons
        for entry in entries:
            text_file.write(entry['description'] + ' Cleartext-Password := "' + entry['password'] + '"\n')
            text_file.write('   Fall-Through == Yes,\n')
            text_file.write('   Service-Type := Framed-User,\n')
            text_file.write('   Framed-Protocol := PPP,\n')
            text_file.write('   Framed-IP-Address := ' + entry['framed_address'] + '\n')
            text_file.write('\n')
        constant_entries = open('/etc/raddb/users.constant').readlines()
        for line in constant_entries:
            text_file.write(line)
        text_file.close()
    except:
        print "oops"