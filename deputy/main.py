#! ../env/bin/python3
from create_keys import create_keys
import paramiko
import sys

def main():
    username = sys.argv[1]
    password = sys.argv[2]
    private_key, public_key = create_keys()

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy)
    client.load_system_host_keys()
    # TODO make this authenticate with a keypair
    client.connect('192.168.184.157', port=12345, username='shf', password='test',
        allow_agent=False, look_for_keys=False)
    stdin, stdout, stderr = client.exec_command('')
    stdin.write(username + '\n')
    stdin.write(password + '\n')
    stdin.write(public_key)
    client.close()

main()
