import paramiko

client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('127.0.0.1', 10022)
# do some operations with client session
client.close()
