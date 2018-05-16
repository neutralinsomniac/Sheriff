import paramiko
import ssh_client
import sys

def main():
    # TODO grab this value from a hosts or a config file
    HOSTNAME = '192.168.184.157'
    PORT = 2200

    sock = ssh_client.open_socket(HOSTNAME, PORT)
    trans = ssh_client.open_transport(sock)
    ssh_client.check_keys(trans, HOSTNAME)
    isAuth = ssh_client.auth_user(trans, HOSTNAME)
    if not isAuth:
        sys.exit(1)
    sftp = paramiko.SFTPClient.from_transport(trans)
    dirlist = sftp.listdir('.')
    print("Dirlist: %s" % dirlist)
    # with sftp.open('../keys/id_rsa-cert.pub', 'r') as f:
    #     data = f.read()
    # with open('~/.ssh/id_rsa-cert.pub', 'w') as f:
    #     f.write(data)
    #ch = ssh_client.open_channel(trans)

if __name__ == '__main__':
    main()
