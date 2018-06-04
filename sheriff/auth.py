# Documentation for the ldap3 library can be found at:
#   http://ldap3.readthedocs.io
from ldap3 import Connection, Server, NTLM
import logging
import config

# Set up logging
logging.basicConfig(filename=config.LOG_FILE, format='%(levelname)s %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

# connect(username, password) where:
#   username is a string containing the username
#   password is a string containing the password
# This method shouldn't fail. conn only fails on conn.bind()
def connect(username, password):
    server = Server(config.ACTIVE_DIRECTORY_SERVER)
    user = config.ACTIVE_DIRECTORY_SERVER + '\\' + username
    conn = Connection(server, user, password, authentication=NTLM)
    return conn

# auth_user(username, password) where:
#   username is a string containing the username
#   password is a string containing the password
#
# returns true if the user is found
# returns false if the user is not
def auth_user(username, password):
    if(len(password) == 0):
        logging.info('User: ' + username + ' did not provide a password')
        return False
    conn = connect(username, password)
    if(conn.bind()):
        logging.info('User: ' + username + ' successfully authenticated')
        return True
    else:
        logging.info('User: ' + username + ' provided invalid username/password')
        return False

# get_user_membership(username, password) where:
#    username is a string containing the username
#    password is a string containing the password
#
# Returns a tuple of membership groups
def get_user_membership(username, password):
    logging.info('Getting group membership for user: ' + username)
    conn = connect(username, password)
    if(conn.bind()):
        conn.search(config.DC_FIELDS,
            '(sAMAccountName=%s)'%username,
            attributes=['memberOf'])
        raw_groups = conn.entries[0].memberOf
        groups = []
        for single_group in raw_groups.values:
            groups.append(single_group.split(',')[0][3:]) # String formatting to pull group names from query return
        return groups
    else:
        # get_user_membership won't be called until after the user has authenticated
        logging.warning('User: ' + username + ' authenticated but could not connect to domain controller for group membership verification' )
        return None
