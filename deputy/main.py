#! ../env/bin/python3
from create_keys import create_keys
import paramiko
import getpass
import config
import ast

def main():
    username = input('Username: ')
    password = getpass.getpass()
    private_key, public_key = create_keys()

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy)
    client.load_system_host_keys()
    # TODO make this authenticate with a keypair
    client.connect(config.HOST_ADDRESS, port=config.HOST_PORT, username=config.CLIENT_USERNAME,
        password=config.CLIENT_PASSWORD, allow_agent=False, look_for_keys=False)
    stdin, stdout, stderr = client.exec_command('')
    stdin.write(username + '\n')
    stdin.write(password + '\n')
    stdin.write(str(public_key) + '\n')
    cert = stdout.readlines()
    print(cert)
    client.close()

    if(len(cert) == 0 or cert[0] == "Invalid username or password"):
        print(cert) #TODO need to handle this error better
        return
        
    with open(username + '_id_rsa.pub', 'wb') as public_file:
        public_file.write(public_key)
    with open(username + '_id_rsa', 'wb') as private_file:
        private_file.write(private_key)
    with open(username + '_id_rsa-cert.pub', 'w') as cert_file:
        cert_file.write(cert[0])

main()
