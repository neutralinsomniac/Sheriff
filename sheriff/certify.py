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
    cert_list = []
    for group_name in groups:
        logging.info('Creating group: ' + group_name + ' certificate for user: ' + username)

        call(['ssh-keygen', '-s', config.SHERIFF_KEYS_DIR + group_name + '_id_rsa',
        '-I', username, '-n', config.CERT_ACCESS_TYPE, '-V', config.CERT_VALIDITY_INTERVAL,
        config.PUB_KEY_DIR_PATH + username +'_id_rsa.pub'])
        
        # Have to rename the cert so it isn't overwritten. ssh-keygen -s doesnt let you determine the output file name
        new_cert = config.PUB_KEY_DIR_PATH + group_name + '_id_rsa-cert.pub'
        try:
            os.rename(config.PUB_KEY_DIR_PATH + username + '_id_rsa-cert.pub', new_cert)
            logging.info('Successfully created certificate in ' + new_cert)
        except OSError as e:
            if(e.errno == errno.ENOENT):
                # certificate couldn't be made
                logging.warning('Certificate for group: ' + group_name + ' could not be made')
            else:
                logging.warning('An exception occured during the creation of the certificate errno: ' + str(e.errno))
        cert_list.append(new_cert)
    return cert_list
