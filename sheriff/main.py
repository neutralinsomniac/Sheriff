import time
import socket
import argparse
import sys
import textwrap

import paramiko

from ssh_server import StubServer, StubSFTPServer

HOST, PORT = '192.168.184.157', 2200 # 0.0.0.0
BACKLOG = 10

def start_server():
    #paramiko_level = getattr(paramiko.common, level)
    #paramiko.common.logging.basicConfig(level=paramiko_level)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    server_socket.bind((HOST, PORT))
    server_socket.listen(BACKLOG)

    while True:
        print('Waiting for Connection...')
        conn, addr = server_socket.accept()
        print('Connection from ' + str(addr))

        host_key = paramiko.RSAKey.from_private_key_file('../keys/id_rsa')
        transport = paramiko.Transport(conn)
        transport.add_server_key(host_key)
        transport.set_subsystem_handler(
            'sftp', paramiko.SFTPServer, StubSFTPServer)

        server = StubServer()
        transport.start_server(server=server)

        channel = transport.accept()
        while transport.is_active():
            time.sleep(1)


# def main():
#     usage = """\
#     usage: sftpserver [options]
#     -k/--keyfile should be specified
#     """
#     parser = argparse.ArgumentParser(usage=textwrap.dedent(usage))
#     parser.add_argument(
#         '--host', dest='host', default=HOST,
#         help='listen on HOST [default: %(default)s]'
#     )
#     parser.add_argument(
#         '-p', '--port', dest='port', type=int, default=PORT,
#         help='listen on PORT [default: %(default)d]'
#     )
#     parser.add_argument(
#         '-l', '--level', dest='level', default='INFO',
#         help='Debug level: WARNING, INFO, DEBUG [default: %(default)s]'
#     )
#     parser.add_argument(
#         '-k', '--keyfile', dest='keyfile', metavar='FILE',
#         help='Path to private key, for example /tmp/test_rsa.key'
#     )
#
#     args = parser.parse_args()
#
#     if args.keyfile is None:
#         parser.print_help()
#         sys.exit(-1)
#
#     start_server(args.host, args.port, args.keyfile, args.level)
#
#
# if __name__ == '__main__':
#     main()
start_server()
