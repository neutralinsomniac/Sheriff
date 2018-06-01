#! ../env/bin/python3
from create_keys import create_keys
from subprocess import PIPE
import subprocess
import getpass
import config

'''
Opens ssh process to CA server
ssh session cannot be opened without signed key from CA

Upon validation of LDAP credentials, private, public and
certificate files are written to:

<ldap-username>_id_rsa
<ldap-username>_id_rsa.pub
<ldap-username>_id_rsa-cert.pub

respectively.
'''

def main():
    username = input('Username: ')
    password = getpass.getpass()
    private_key, public_key = create_keys()
    args = ['ssh', config.CLIENT_USERNAME + '@192.168.184.157', '-p', '12345']

    with subprocess.Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True) as proc:
        proc.stdin.write(username + '\n')
        proc.stdin.write(password + '\n')
        proc.stdin.write(public_key.decode('utf-8')+'\n')
        proc.stdin.flush()
        sheriff_responses = proc.stdout.readlines()

    with open(username + '_id_rsa', 'wb') as private_key_file:
        private_key_file.write(private_key)

    with open(username + '_id_rsa.pub', 'wb') as public_key_file:
        public_key_file.write(public_key)

    with open(username + '_id_rsa-cert.pub', 'w') as cert_file:
        cert_file.write(sheriff_responses[-1])

main()
