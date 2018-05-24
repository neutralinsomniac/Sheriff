#! /usr/bin/env python3
from auth import auth_user
import certify
import os, errno
import getpass

def main():
    username = input()
    password = input()
    publicKey = input()
    if not os.path.exists('/tmp/Sheriff_Public_Keys'):
        try:
            os.makedirs('/tmp/Sheriff_Public_Keys')
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    #TODO Error handling!
    if(auth_user(username, password)):
        with open('/tmp/Sheriff_Public_Keys/id_rsa.pub', 'w') as fl:
            fl.write(publicKey[2:-1])# get rid of the singlequotes and b on the endpoints
        certify.create_certificate(username)
        with open('/tmp/Sheriff_Public_Keys/id_rsa-cert.pub', 'r') as cert:
            print(cert.read())

    else:
        print("Invalid username or password")

main()
