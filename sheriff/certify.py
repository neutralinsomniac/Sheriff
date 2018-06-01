from subprocess import Popen, PIPE
import os, errno
import logging
import config

# def create_certificates(username, groups):
#   username - (ldap) username of user requesting certificates
#   groups - list of groups user belongs to that need certificates
# create_certificates calls ssh-keygen via the command line

def create_certificates(username, groups):
    logging.basicConfig(filename=config.LOG_FILE, format='%(levelname)s %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
    public_key = ''
    logging.info('Creating certificate for user: ' + username + ' in groups: ' + str(groups))

    groupList = ','.join(groups)
    args = ['ssh-keygen', '-s', config.SHERIFF_SIGNING_KEY, '-I', username,
        '-n', groupList, '-V', config.CERT_VALIDITY_INTERVAL,
        config.PUB_KEY_DIR_PATH + username +'_id_rsa.pub']

    proc = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate() # For some reason ssh-keygen -s outputs to stderr regardless of success. Use err for logging
    new_cert = config.PUB_KEY_DIR_PATH + username + '_id_rsa-cert.pub'
    
    if(os.path.isfile(new_cert)):
        logging.info('Certificate: ' + new_cert + ' was successfully created')
    else:
        logging.warning('Certificate creation failed: ' + err.decode('utf-8'))

    return new_cert
