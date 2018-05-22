#! /usr/bin/env python3
from auth import auth_user
import certify
import os

def main():
    username = input()
    password = input()
    publicKey = input()
    print(os.getcwd())
    if(auth_user(username, password)):
        with open('/home/sheriff/Desktop/Sheriff/sheriff/tmp.pub', 'w') as fl:
            fl.write(str(publicKey))
        certify.create_certificate(username)
    else:
        print("Invalid username or password")


main()
