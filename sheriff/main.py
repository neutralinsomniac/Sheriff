import os
import socket
import sys
import threading

import paramiko

def main():
    paramiko.util.log_to_file('sheriff_server.log')
    host_key = paramiko.RSAKey(filename='sheriff_rsa.key')
