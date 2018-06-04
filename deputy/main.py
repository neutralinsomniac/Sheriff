#! ../env/bin/python3
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

def create_keys(username):
    subprocess.Popen(['./create_keys.sh', username]).wait()
    with open(username + "_id_rsa", 'r') as priv_key_file:
        priv_key = priv_key_file.read()

    with open(username + "_id_rsa.pub") as pub_key_file:
        pub_key = pub_key_file.read()

    return pub_key

def main():
    username = input('Username: ')
    password = getpass.getpass()
    public_key = create_keys(username)
    args = ['ssh', config.CLIENT_USERNAME + '@192.168.184.157', '-p', '12345']

    with subprocess.Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True) as proc:
        proc.stdin.write(username + '\n')
        proc.stdin.write(password + '\n')
        proc.stdin.write(public_key +'\n')
        proc.stdin.flush()
        sheriff_responses = proc.stdout.readlines()

    if(str(sheriff_responses[-1]) == 'False\n'):
        print('Invalid username/password: Certificate could not be created.')
        return

    with open(username + '_id_rsa-cert.pub', 'w') as cert_file:
        cert_file.write(sheriff_responses[-1])

main()
