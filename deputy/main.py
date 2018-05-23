#! ../env/bin/python3
from create_keys import create_keys
import paramiko

def main():
    username = 'jack.daniels' #input('Username: ')
    password = 'Whi$key' #input('Password: ')
    private_key, public_key = create_keys()

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy)
    client.load_system_host_keys()
    # TODO make this authenticate with a keypair
    client.connect('192.168.184.157', port=12345, username='sheriff_server',
        password='test', allow_agent=False, look_for_keys=False)
    stdin, stdout, stderr = client.exec_command('')
    stdin.write(username + '\n')
    stdin.write(password + '\n')
    stdin.write(str(public_key) + '\n')
    cert = stdout.readlines()[0]
    client.close()
    print('\n Public Key: ')
    print(public_key)
    print('\n Private Key: ')
    print(private_key)
    print('\n Certificate: ')
    print(cert)
    with open('id_rsa.pub', 'wb') as public_file:
        public_file.write(public_key)
    with open('id_rsa', 'wb') as private_file:
        private_file.write(private_key)
    with open('id_rsa-cert.pub', 'w') as cert_file:
        cert_file.write(cert)


main()
