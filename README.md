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

server_ca     - certificate authority private key. used to sign the machines ssh_host_rsa_key.pub to create certificate for the CA
server_ca.pub - certificate authority public key. used to verify hosts to the clients

ssh_host_rsa_key-cert.pub - certificate created with server_ca(generated) and ssh_host_rsa_key.pub(pre-installed)
	- this certificiate needs to be on the CA server as well as all hosts
		- sshd_config is configured to trust this certificate with the following line:
			HostCertificate <path_to_ssh_host_key-cert.pub>

users_ca     - certificate authority's keyset for authenticating users
users_ca.pub - certificate authority's keyset for authenticating users
	** user will send it's own public key (id_rsa.pub) to certificate authority where it will be signed with users_ca
		ex.) ssh-keygen -s users_ca -I <username_computername> -n root id_rsa.pub

	** users_ca.pub will have to be trusted by all ssh hosts. This is done by copying users_ca.pub from the certificate authority
		to the host machine and configuring the host machine to trust this key with the following line:
			TrustedUserCAKeys <path_to_users_ca.pub>

id_rsa	   - Client private key
		prefereably stored in ~/.ssh
id_rsa.pub - client public key
		preferably stored in ~/.ssh
	** this file is sent to the Certificate authority and signed with users_ca. The newly generated:
		id_rsa-cert.pub
		is the certificate that will be sent back to the client and used as authorization to ssh into the machine


What has to be done on the CA
	1.) The certificate authority is responsible for creating the keys that validate both the servers and the clients
		server_ca and server_ca.pub
			as well as
		users_ca and users_ca.pub
	2.) Before the CA can start signing certificates and issuing trust, it needs to sign a certificate for itself. This is
	done with server_ca and ssh_host_rsa_key-cert.pub (ssh-keygen -s server_ca -I <identity> -h ssh_host_rsa_key.pub)
	3.) The resulting certificate needs to be configured as a HostCertificate in sshd_conf on both the CA Server and all Hosts
	4.) The user public key needs to be shared with hosts so they know to trust signed keys
	5.) Take client public keys and authorize them by signing them with certificates (handled by Sheriff/Deputy)

What has to be done on the Host
	1.) Recieve ssh_host_rsa_key-cert.pub and configure the certificate as a HostCertificate
	2.) Recieve users_ca.pub and configure the public key as a TrustedUserCAKeys

What has to be done on the Client (1 and 2 handled by Deputy)
	1.) send the Certificate authority a public key for signing (authentication on CA server)
		** make sure key pair is added with ssh-add <private-key>
	2.) receive Cert and place it in ~/.ssh
	3.) ssh into Host


Config:
