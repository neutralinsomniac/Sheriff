import base64
from binascii import hexlify
import getpass
import os
import select
import socket
import sys
import time
import traceback
import paramiko
from paramiko.py3compat import input

# setup logging TODO maybe put this and some of the other stuff in an init function
paramiko.util.log_to_file('sheriff.log')

# TODO This might not be necessary
try:
    import interactive
except ImportError:
    from . import interactive

#Probably won't be used but necessary for ssh key auth
def agent_auth(transport, username):
    """
    Attempt to authenticate to the given transport using any of the private
    keys available from an SSH agent.
    """

    agent = paramiko.Agent()
    agent_keys = agent.get_keys()
    if len(agent_keys) == 0:
        return

    for key in agent_keys:
        print('Trying ssh-agent key %s' % hexlify(key.get_fingerprint()))
        try:
            transport.auth_publickey(username, key)
            print('... success')
            return
        except paramiko.SSHException:
            print('... nope.')


def manual_auth(username, hostname, t):
    pw = getpass.getpass('Password for %s@%s: ' % (username, hostname))
    t.auth_password(username, pw)

# open_socket(hostname, port)
#   INPUT hostname - ipaddress or hostname known to client
#         port - port that the server is using
#   RETURNS connected socket
def open_socket(hostname, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((hostname, port)) # TODO change this to input at some point
        return sock
    except Exception as e:
        # Socket couldn't be opened - probably due to bad hostname(ipaddress)
        print('*** Connect failed: ' + str(e))
        traceback.print_exc()
        #sys.exit(1)
        return False

def open_transport(sock):
    t = paramiko.Transport(sock)
    try:
        t.start_client()
        return t
    except paramiko.SSHException:
        return False

def check_keys(t, hostname):
    try:
        keys = paramiko.util.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
    except IOError:
        try:
            keys = paramiko.util.load_host_keys(os.path.expanduser('~/ssh/known_hosts'))
        except IOError:
            print('*** Unable to open host keys file')
            keys = {}

    # check server's host key -- this is important.
    key = t.get_remote_server_key()
    print(hexlify(key.get_fingerprint()))
    if hostname not in keys:
        print('*** WARNING: Unknown host key!')
    elif key.get_name() not in keys[hostname]:
        print('*** WARNING: Unknown host key!')
    elif keys[hostname][key.get_name()] != key:
        print('*** WARNING: Host key has changed!!!')
        False
        #sys.exit(1)
    else:
        print('*** Host key OK.')

def auth_user(t, hostname):
    # get username
    default_username = getpass.getuser()
    username = input('Username [%s]: ' % default_username)
    if len(username) == 0:
        username = default_username

    manual_auth(username, hostname, t)
    if not t.is_authenticated():
        print('*** Authentication failed. :(')
        t.close()
        return False
        #sys.exit(1)
    return True

# make sure to crate a sftp channel
# def open_channel(trans):
#     chan = t.open_session()
#     chan.get_pty()
#     chan.invoke_shell()
#     print('*** Here we go!\n')
#     interactive.interactive_shell(chan)
#     chan.close()
#     t.close()

# except Exception as e:
#     print('*** Caught exception: ' + str(e.__class__) + ': ' + str(e))
#     traceback.print_exc()
#     try:
#         t.close()
#     except:
#         pass
#     sys.exit(1)
