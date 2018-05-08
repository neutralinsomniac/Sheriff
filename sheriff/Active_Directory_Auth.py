#from ldap3 import Connection

##########################
## Anonymous connection ##
# print('Connecting to Active Directory...')
#
# try:
#     conn = Connection('bastion.local', auto_bind=True)
#     print('Connection Successful!')
# except e:
#     print(e)
#
# print(conn)

##############################
## Authenticated connection ##
from ldap3 import Server, Connection, NTLM, ALL
server = Server('bastion.local')
conn = Connection(server, user='bastion.local\\john.doe', password='Pa$$word13', authentication=NTLM)
conn.bind()
print(conn.extend.standard.who_am_i())
