from ldap3 import Connection, Server, NTLM, ALL, ObjectDef
from ldap3.core import exceptions

DC = ['bastion', 'local']
ACTIVE_DIRECTORY_SERVER = 'bastion.local'

def auth_user(username, password):
    server = Server(ACTIVE_DIRECTORY_SERVER)
    user = ACTIVE_DIRECTORY_SERVER + '\\' + username
    conn = Connection(server, user, password, authentication=NTLM)
    if(conn.bind()):
        conn.search('dc=%s, dc=%s'%(DC[0],DC[1]),
            '(sAMAccountName=%s)'%username,
            attributes=['memberOf'])
        return conn.entries[0].memberOf
    else:
        return None
