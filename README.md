# Sheriff
Sheriff is a certificate authority utility that administers certificates through Active Directory authentication. Sheriff was built for Linux systems and specifically tested on Ubuntu 16.04. The sheriff server files and scripts can be found in **Sheriff/sheriff**.

# Deputy
Deputy is the client side utility used to request certificates from Sheriff with Active Directory credentials. The deputy files and scripts can be found in **Sheriff/deputy**

## Configurations

### Sheriff CA Configurations
* Copy **Sheriff/sheriff** to **/opt** (/opt/sheriff) directory
* Create a soft link from **/opt/sheriff/main.py** to **/usr/local/bin/sheriff**

	`ln -s /opt/sheriff/main.py /usr/local/bin/sheriff`

* Create user on the certificate authority machine that matches the CLIENT_USERNAME constant in the deputy/config.py file, and set his shell to be /usr/local/bin/sheriff:

	`useradd -s /usr/local/bin/sheriff sheriff_server`

* Create directory **/opt/sheriff/CA_Keys** and give new user *sheriff_server* ownership of **CA_Keys**:
	```
	mkdir /opt/sheriff/CA_Keys
	chown sheriff_server /opt/sheriff/CA_Keys
	```

### Sheriff CA SSH Configurations
* In the **/opt/sheriff/CA_Keys** directory, create three key pairs using the ssh-keygen command
	* One will be the server keypair that is used to authenticate the ssh hosts
	* One will be the user keypair that is used to authenticate the users to the ssh hosts
	* One will be the client keypair that is used to authenticate the clients to the CA
* This can be done with the following commands:
	```
	ssh-keygen -f /opt/sheriff/CA_Keys/server_ca
	ssh-keygen -f /opt/sheriff/CA_Keys/users_ca
	ssh-keygen -f /opt/sheriff/CA_Keys/client_ca
	```

* Have the CA sign its own certificate with **server_ca** (private key) and **/etc/ssh/ssh_host_rsa_key.pub**:

	`ssh-keygen -s /opt/sheriff/CA_Keys/server_ca -I sheriff_server -h -n sheriff_server /etc/ssh/ssh_host_rsa_key.pub`

	* This should create the following: **/etc/ssh/ssh_host_rsa_key-cert.pub**
	* Configure this file as the **HostCertificate** in the **/etc/ssh/sshd_config** file by adding this line:

	`HostCertificate /etc/ssh/sshd_host_rsa_key-cert.pub`

* Now the CA has to sign certificates for the ssh hosts. On the ssh host machine, copy **/etc/ssh/ssh_host_rsa_key.pub** to the CA and sign it with the **server_ca** private key:

	`ssh-keygen -s /opt/sheriff/CA_Keys/server_ca -i sheriff_server -h -n sheriff_server <path_to_copied_ssh_host_key_file>`

	* Copy the newly created **ssh_host_rsa_key-cert.pub** that was created with the hosts public key back to the ssh host machine's **/etc/ssh/** directory

* In order for the clients to be able to communicate with the CA server to request certificates, they need to be authorized. This will be done by signing certificates with the **client_ca** keypair
	* Copy **users_ca.pub** (public key) to the CA servers **/etc/ssh/** directory
	* Add **users_ca.pub** to the TrustedUserCAKeys by adding the following line to the CA Servers **/etc/ssh/sshd_config** file:

	`TrustedUserCAKeys /etc/ssh/users_ca.pub`

	* On the client machine, create a keypair for signing with the following ssh-keygen command:
	`ssh-keygen -f ~/.ssh/deputy_id_rsa`

	and copy the public key (**deputy_id_rsa.pub**) to the CA Server for signing.
		
	* On the CA server, sign **deputy_id_rsa.pub** with the **/opt/sheriff/CA_Keys/client_ca** (client private key) file with the following command:
		`ssh-keygen -s /opt/sheriff/CA_Keys/client_ca -I deputy_Client -n sheriff_server <path_to_deputy_id_rsa.pub>`

		This will create a certificate **deputy_id_rsa-cert.pub** to allow clients to request ssh host authorization. Copy this cert back to the client machine.

### Host SSH Configurations
*  Configure the signed ssh_host_rsa_key as a **HostCertificate** on the ssh host's **/etc/ssh/sshd_config** file by adding the following line:
	`HostCertificate /etc/ssh/ssh_host_rsa_key-cert.pub`

* Copy the CA server's user public key (**CA: /opt/sheriff/CA_Keys/users_ca.pub**) to the ssh-host's **/etc/ssh/** directory and configure it as a **TrustedUserCAKey** by adding the following line to the **/etc/ssh/sshd_config** file:
	`TrustedUserCAKeys /etc/ssh/users_ca.pub`

* To limit the host to certain Active Directory groups, create a directory in **/etc/ssh/** for all authorized certificate principals. Call this directory **auth_principals**

* Add a file in **/etc/ssh/auth_principals** that tells ssh what certificate principals are authorized as local users. To authorize certificate principals as root users, create the file **/etc/ssh/auth_principals/root** and add the principals that are permitted to login as root. In this case, the principals will be the corresponding Active Directory groups for the host machine.

* Configure sshd_config to allow these authorized principals by adding the following line to the hosts **/etc/ssh/sshd_config** file:
	`AuthorizedPrincipalsFile /etc/ssh/auth_principals/%u`

	%u is replaced with the local account being authorized on the ssh host. In this case, the local account will be root.

### Client Configurations
* Using the previously created **deputy_id_rsa-cert.pub** certificate, move it to the **~/.ssh/** directory and add it to the ssh-agent with the following command:
	`ssh-add deputy_id_rsa`

This will allow the clients to communicate with the CA server

### Active Directory Configurations
All of the Active Directory configuration parameters can be adjusted in the **sheriff/config.py**

### SSH Configurations
Optionally, the CA Server and SSH Servers can be configured to disable password authentication. This can be done by setting the **/etc/ssh/sshd_config** **PasswordAuthentication** field to **no**

## Running Sheriff
By configuring the account sheriff_server to execute **/usr/local/bin/sheriff** (which is a soft link to **/opt/sheriff/main.py**) on login, we can send a request for authorization via ssh. The ssh configurations can be found in **deputy/config.py**.

## Running Deputy
Run **python3 deputy/main.py** at which point you will be prompted for a username and password. Deputy will then generate a key-pair and send the public key, username and password to Sheriff. If authentication is successful, deputy will create three files in **deputy/**. These files will contain the public, private, and certificate information for remote ssh access. The files will be named as follows:
* < username >\_id\_rsa (private key)
* < username >\_id\_rsa.pub (public key)
* < username >\_id\_rsa-cert.pub (certificate file)

The private key needs to have the permissions locked down. This can be done with:
	`chown 600 < username >\_id\_rsa (private key)`

These files should be copied to **~/.ssh/** and added with the following command:
	`ssh-add -t 30m < username >\_id\_rsa`

**\*Note** -t 30m only adds the certificates for 30 minutes. Be sure to configure this to whatever the time is set as the **CERT_VALIDITY_INTERVAL** in **/sheriff/config.py**  
