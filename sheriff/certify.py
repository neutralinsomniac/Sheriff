from subprocess import call
import datetime
import os

# TODO: implement config file that determines how long the interval is
# and what users get what permissions

#def create_certificate(membership, username):
def create_certificate(username):
    call(['ssh-keygen', '-s', '/opt/Sheriff/CA_keys/users_ca', '-I', 'deputy', '-n',
        "root", '-V', '-1m:+30m', '/tmp/Sheriff_Public_Keys/id_rsa.pub'])
