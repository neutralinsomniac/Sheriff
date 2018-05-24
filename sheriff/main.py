#! /usr/bin/env python3
from auth import auth_user, get_user_membership
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
        groups = get_user_membership()
        if(len(groups) = 0):
            print('User is not a member of any recognized groups')
            print('Either add user to group or update Sheriff Group List')
            return
        with open('/tmp/Sheriff_Public_Keys/id_rsa.pub', 'w') as fl:
            fl.write(publicKey[2:-1]) # get rid of the singlequotes and b on the endpoints
        cert_list = certify.create_certificates(username, groups)
        for path in cert_list:
            with open(path, 'r') as cert:
                print(cert.read())

    else:
        print('Invalid username or password')
        return

main()
