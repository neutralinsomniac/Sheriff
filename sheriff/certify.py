from subprocess import call
import datetime
import logging
import os, errno
import config

# def create_certificates(username, groups):
#   username - (ldap) username of user requesting certificates
#   groups - list of groups user belongs to that need certificates
# create_certificates calls ssh-keygen via the command line
def create_certificates(username, groups):
    logging.basicConfig(filename=config.LOG_FILE, format='%(levelname)s %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
    public_key = ''
    logging.info('Creating certificate for user: ' + username + ' in groups: ' + str(groups))

    groupList = ''
    for group in groups:
        groupList += group + ','
    groupList = groupList[:-1]

    call(['ssh-keygen', '-s', config.SHERIFF_SIGNING_KEY, '-I', username,
    '-n', groupList, '-V', config.CERT_VALIDITY_INTERVAL,
    config.PUB_KEY_DIR_PATH + username +'_id_rsa.pub'])

    # Have to rename the cert so it isn't overwritten. ssh-keygen -s doesnt let you determine the output file name
    new_cert = config.PUB_KEY_DIR_PATH + username + '_id_rsa-cert.pub'
    if(os.path.isfile(new_cert)):
        logging.info('Certificate: ' + new_cert + ' was successfully created')
    else:
        logging.warning('Certificate creation failed')
    return new_cert
