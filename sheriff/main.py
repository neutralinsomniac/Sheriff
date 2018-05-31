#! /usr/bin/env python3
from auth import auth_user, get_user_membership
from subprocess import call
import certify
import os, errno
import getpass
import logging
import config

def main():
    # Set up logging
    logging.basicConfig(filename=config.LOG_FILE, format='%(levelname)s %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
    username = input()
    password = input()
    publicKey = input()

    logging.info('Received Connection from ' + username)
    if not os.path.exists(config.PUB_KEY_DIR_PATH):
        try:
            logging.info('Creating temporary key directory')
            os.makedirs(config.PUB_KEY_DIR_PATH)
        except OSError as e:
            if e.errno != errno.EEXIST:
                logging.warning(e)
                raise
            else:
                logging.warning('Temporary Directory was not cleared by last user')
    if(auth_user(username, password)):
        groups = get_user_membership(username, password)
        if(len(groups) == 0):
            logging.info('User: ' + username + ' is not a member of any known groups')
            print('User is not a member of any recognized groups')
            return
        logging.info('Saving user public key in /tmp/Sheriff_Public_Keys/' + username +'_id_rsa.pub ')
        # Add username to public key to keep them unique
        with open(config.PUB_KEY_DIR_PATH + username +'_id_rsa.pub', 'w') as fl:
            fl.write(publicKey) # get rid of the singlequotes and b on the endpoints
        logging.info('Creating certificate for user ' + username)
        cert_path = certify.create_certificates(username, groups)
        with open(cert_path, 'r') as cert:
            print(cert.read(), end='')
        call(['rm', '-rf', config.PUB_KEY_DIR_PATH])
    else:
        print('Invalid username or password')
        return

main()
