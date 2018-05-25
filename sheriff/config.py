# Configuration settings for global constants

LOG_FILE = '/opt/Sheriff/Logs/Sheriff.log'
PUB_KEY_DIR_PATH = '/tmp/Sheriff_Public_Keys/' #TODO make sure this should/shouldn't trail with a /
CERT_VALIDITY_INTERVAL = '-1m:+30m' # 1 minute ago to 30 minutes from now
CERT_ACCESS_TYPE = 'root'
SHERIFF_KEYS_DIR = '/opt/Sheriff/CA_keys/'
DC_FIELDS = 'dc=bastion,dc=local'
ACTIVE_DIRECTORY_SERVER = 'bastion.local'
KEY_SIZE = 2048
