# Configuration settings for global constants

LOG_FILE = '/opt/Sheriff/Logs/Sheriff.log'
PUB_KEY_DIR_PATH = '/tmp/Sheriff_Public_Keys/'
CERT_VALIDITY_INTERVAL = '-1m:+30m' # 1 minute ago to 30 minutes from now
SHERIFF_SIGNING_KEY = '/opt/Sheriff/CA_keys/users_ca'
DC_FIELDS = 'dc=bastion,dc=local'
ACTIVE_DIRECTORY_SERVER = 'bastion.local'
KEY_SIZE = 2048
