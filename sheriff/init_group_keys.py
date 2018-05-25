from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend
from os import environ, chmod
from subprocess import call
from auth import connect
import config

def init():
    username = input('Username: ')
    password = input('Password: ')
    conn = connect(username, password)
    conn.bind()
    conn.search(config.DC_FIEDS,'(objectclass=group)',attributes=['cn'])
    cn_object_list = conn.entries
    cn_name_list = []
    for cn_object in cn_object_list:
        cur_name = str(cn_object.CN).replace(' ', '_').replace('-', '_')
        print('Creating keypair for group ' + cur_name + '...')
        create_key_pair(cur_name)
        print("Done.")

def create_key_pair(group_name):

    key = rsa.generate_private_key(
        backend=crypto_default_backend(),
        public_exponent=65537,
        key_size=config.KEY_SIZE
    )

    privkey = key.private_bytes(
        crypto_serialization.Encoding.PEM,
        crypto_serialization.PrivateFormat.PKCS8,
        crypto_serialization.NoEncryption())

    pubkey = key.public_key().public_bytes(
        crypto_serialization.Encoding.OpenSSH,
        crypto_serialization.PublicFormat.OpenSSH
    )

    with open(config.SHERIFF_KEYS_DIR + group_name + '_id_rsa', 'wb') as priv_key_file:
        priv_key_file.write(privkey)

    with open(config.SHERIFF_KEYS_DIR + group_name + '_id_rsa.pub', 'wb') as pub_key_file:
        pub_key_file.write(pubkey)

init()
