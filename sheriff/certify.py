from subprocess import call
import datetime

# TODO: implement config file that determines how long the interval is
# and what users get what permissions

def create_certificate(membership, username):
    call(['ssh-keygen', '-s', '~/.ssh/host_ca', '-I', username, '-V', timeinterval(15), ])

def time_in_n_minutes(n):
    x = str(datetime.datetime.now() + datetime.timedelta(0, (n*60)))
    y = x.replace('-', '').replace(' ', '').replace('.', '').replace(':', '')
    return y[:-6]

def timeinterval(minutes):
    cur_time = time_in_n_minutes(0)
    end_time = time_in_n_minutes(minutes)
    interval = cur_time + ':' + end_time
    return interval
