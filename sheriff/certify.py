from subprocess import call
import datetime

# TODO: implement config file that determines how long the interval is
# and what users get what permissions

#def create_certificate(membership, username):
def create_certificate(username):
    auth_level = 'root'
    call(['ssh-keygen', '-s', '../keys/host', '-I', username, '-n',
        auth_level, '-V', '-1m:+30m', '../keys/id_rsa.pub'])
