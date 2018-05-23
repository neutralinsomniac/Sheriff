from subprocess import call
import datetime

# TODO: implement config file that determines how long the interval is
# and what users get what permissions

#def create_certificate(membership, username):
def create_certificate(username):
    call(['ssh-keygen', '-s', '../CA_keys/users_ca', '-I', username, '-n',
        "root", '-V', '-1m:+30m', './temp.pub'])
