from create_keys import create_keys
import paramiko
import ssh_client
import sys
import os

# def testCallback(sent, total):
#     print('sent: ' + str(sent))
#     print('total: ' + str(total))

def main():
    user = 'jack.daniels'#input("Username: ")
    passwrd = 'Whi$key'#input("Password: ")
    transport = paramiko.Transport(('192.168.184.157', 2200))
    try:
        transport.connect(username = user, password = passwrd)
        sftp = paramiko.SFTPClient.from_transport(transport)
        #public_key = create_keys()
        sftp.put('./id_rsa.pub', '')
        # file_name = '../keys/id_rsa-cert.pub'
        # sftp.get(file_name, './id_rsa-cert.pub')
        sftp.close()
        transport.close()
        return True
    except Exception as e:
        print(e)
        sftp.close()
        transport.close()
        return False

main()
