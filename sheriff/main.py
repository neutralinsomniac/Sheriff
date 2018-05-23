#! /usr/bin/env python3
from auth import auth_user
import certify
import os
import getpass

def main():
    username = 'jack.daniels'#input()
    password = 'Whi$key'#input()
    publicKey = '12345'#input()
    print(getpass.getuser())
    if(auth_user(username, password)):
        with open(os.getcwd() + '/client_keys/test.txt', 'r') as fl:
            print(fl.read())
        # certify.create_certificate(username)
        # with open(os.getcwd() + '/client_keys/temp-cert.pub', 'r') as cert:
        #     print(cert.readlines()[0])
    else:
        print("Invalid username or password")

main()
