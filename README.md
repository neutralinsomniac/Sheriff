Sheriff - the ssh certificate authentication adminstrator
Deputy - a Sheriff client


This project uses a virtual environment in the root directory


virtualenv can installed with:
python3 -m pip install --user virtualenv

The virtual environment needs to then be create with:
python3 -m virtualenv %dirName%

You can enter the virtual environment with:
source %dirName$/bin/activate

and exit with:
exit


all requirements can be found in:
requirements.txt

TODO LIST:
1.) Active Directory authentication needs to be on use_ssl


y
Issue with install python-gssapi:

If the install system uses Heimdal Kerberos, then the gssapi isntaller won't be able to find the 
required configuration files. To remedy this use the following commands:

$ sudo ln -s /usr/bin/krb5-config.mit /usr/bin/krb5-config
$ sudo ln -s /usr/lib/x86_64-linux-gnu/libgssapi_krb5.so.2 /usr/lib/libgssapi_krb5.so
$ sudo apt-get install python-pip libkrb5-dev
$ sudo pip install gssapi

more information can be seen here:
https://stackoverflow.com/questions/30896343/how-to-install-gssapi-python-module?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
