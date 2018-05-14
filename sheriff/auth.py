# Documentation for the ldap3 library can be found at:
#   http://ldap3.readthedocs.io
from ldap3 import Connection, Server, NTLM

# DC is a constant regarding the DC fields of the Active Directory server
DC = ['bastion', 'local']

#ACTIVE_DIRECTORY_SERVER is a constant with the domain name of the active director server
ACTIVE_DIRECTORY_SERVER = 'bastion.local'

# build_search_base_string() builds the query string based on the DC constant.
def build_search_base_string():
    search_base = ''
    for i in DC:
        search_base = search_base + 'dc=%s,'%i
    return(search_base[0:-1])

# auth_user(username, password) where:
#   username is a string containing the username
#   password is a string containing the password
#
# returns true if the user is found
# returns false if the user is not
def auth_user(username, password):
    if(len(password) == 0):
        return False
    server = Server(ACTIVE_DIRECTORY_SERVER)
    user = ACTIVE_DIRECTORY_SERVER + '\\' + username
    conn = Connection(server, user, password, authentication=NTLM)
    if(conn.bind()):
        return True
        # conn.search(build_search_base_string(),
        #     '(sAMAccountName=%s)'%username,
        #     attributes=['memberOf'])
        # return conn.entries[0].memberOf
    else:
        return False

# get_user_membership(username, password) where:
#    username is a string containing the username
#    password is a string containing the password
#
# Returns a tuple of membership groups
def get_user_membership(username, password):
    server = Server(ACTIVE_DIRECTORY_SERVER)
    user = ACTIVE_DIRECTORY_SERVER + '\\' + username
    conn = Connection(server, user, password, authentication=NTLM)
    if(conn.bind()):
        conn.search(build_search_base_string(),
            '(sAMAccountName=%s)'%username,
            attributes=['memberOf'])
        return conn.entries[0].memberOf
