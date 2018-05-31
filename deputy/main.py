#! ../env/bin/python3
from create_keys import create_keys
import paramiko
import getpass
import config
import ast

'''
Opens ssh process to certificate authority
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
    args = ['ssh', 'sheriff_server@192.168.184.157', '-p', '12345']

    with subprocess.Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True) as proc:
        proc.stdin.write(username + '\n')
        proc.stdin.write(password + '\n')
        proc.stdin.write(publicKey.decode('utf-8')+'\n')
        proc.stdin.flush()
        sheriff_responses = proc.stdout.readlines()

    with open(username + '_id_rsa', 'wb') as private_key_file:
        privateKey_file.write(private_key)

    with open(username + '_id_rsa.pub', 'wb') as public_key_file:
        publicKey_file.write(public_key)

    with open(username + '_id_rsa-cert.pub', 'w') as cert_file:
        cert_file.write(sheriff_responses[-1])

main()
