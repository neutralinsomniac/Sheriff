from subprocess import call
import datetime
import os

VALIDITY_INTERVAL = '-1m:+30m'

# TODO: implement config file that determines how long the interval is
# and what users get what permissions

#def create_certificate(membership, username):
def create_certificates(username, groups):
    public_key = ''
    cert_list = []
    for i in groups:
        call(['ssh-keygen', '-s', '/opt/Sheriff/CA_keys/'+i+'_id_rsa',
        '-I', username, '-n', 'root', '-V', VALIDITY_INTERVAL,
        '/tmp/Sheriff_Public_Keys/id_rsa.pub'])
        # Have to rename the cert so it isn't overwritten. ssh-keygen -s doesnt let you determine the output file name
        new_cert = 'tmp/Sheriff_Public_Keys/' + i + '_id_rsa-cert.pub'
        os.rename('/tmp/Sheriff_Public_Keys/id_rsa-cert.pub',
        new_cert)
        cert_list.append(new_cert)
    return cert_list
