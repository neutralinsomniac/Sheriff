import base64
from binascii import hexlify
import getpass
import os
import select
import socket
import sys
import time
import traceback
from paramiko.py3compat import input

import paramiko
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


def manual_auth(username, hostname):
    pw = getpass.getpass('Password for %s@%s: ' % (username, hostname))
    t.auth_password(username, pw)


# setup logging
paramiko.util.log_to_file('demo.log')

hostname = '192.168.184.157'
port = 2200
# now connect
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((hostname, port))
except Exception as e:
    print('*** Connect failed: ' + str(e))
    traceback.print_exc()
    sys.exit(1)

try:
    t = paramiko.Transport(sock)
    try:
        t.start_client()
    except paramiko.SSHException:
        print('*** SSH negotiation failed.')
        sys.exit(1)

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
        sys.exit(1)
    else:
        print('*** Host key OK.')

    # get username
    default_username = getpass.getuser()
    username = input('Username [%s]: ' % default_username)
    if len(username) == 0:
        username = default_username

    manual_auth(username, hostname)
    if not t.is_authenticated():
        print('*** Authentication failed. :(')
        t.close()
        sys.exit(1)

    chan = t.open_session()
    chan.get_pty()
    chan.invoke_shell()
    print('*** Here we go!\n')
    interactive.interactive_shell(chan)
    chan.close()
    t.close()

except Exception as e:
    print('*** Caught exception: ' + str(e.__class__) + ': ' + str(e))
    traceback.print_exc()
    try:
        t.close()
    except:
        pass
    sys.exit(1)
