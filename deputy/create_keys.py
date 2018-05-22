from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend
from os import environ, chmod
from subprocess import call

def create_keys():
    homedir = environ['HOME']

    key = rsa.generate_private_key(
        backend=crypto_default_backend(),
        public_exponent=65537,
        key_size=2048
    )
    privkey = key.private_bytes(
        crypto_serialization.Encoding.PEM,
        crypto_serialization.PrivateFormat.PKCS8,
        crypto_serialization.NoEncryption())

    pubkey = key.public_key().public_bytes(
        crypto_serialization.Encoding.OpenSSH,
        crypto_serialization.PublicFormat.OpenSSH
    )

    #ssh_add_new_key(homedir + '/.ssh/id_rsa')

    return privkey, pubkey

def ssh_add_new_key(keypath):
    call(['ssh-add', keypath]) #Optional Silence: , '2>/dev/null'])
