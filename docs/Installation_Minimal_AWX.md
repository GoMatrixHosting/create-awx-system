# GoMatrixHosting AWX Setup - Minimal Installation Instructions

How to install this AWX setup without a front-end wordpress site, digitalocean service, graphana monitor, or backup server.

# Create a server

Create a Debian 10 server and setup SSH access to root user.
```
$ ssh root@panel.example.org
$ exit
```

# Setup DNS entry for it:

Map an A record for panel.example.org to the servers IP.


# Installation

Installation is broken up into 5 stages:

1) Pre-setup, setup before the awx playbook is run, installs Docker and sets up TLS proxy for AWX, optionally website hooks and grafana are also setup.

`$ git clone https://gitlab.com/GoMatrixHosting/create-awx-system.git`

Install prerequisite packages for ansible on the controller:

`$ ansible-galaxy collection install community.grafana`

Edit host into: ./inventory/hosts

Create folder for host at: ./inventory/host_vars/panel.example.org/

Record these variables to ./inventory/host_vars/panel.example.org/vars.yml:
- org_name 			(The name of your organisation.)
- awx_url 			(The URL for AWX.)
- certbot_email 		(The organisations email.)
- admin_password 		(Strong password for the AWX admin user.)
- create_delete_source		(Repository URL for 'Ansible Create Delete Subscription Membership'.)
- create_delete_branch		(Branch of this repository to use.)
- provision_source		(Repository URL for 'Ansible Provision'.)
- provision_branch		(Branch of this repository to use.)
- deploy_source			(Repository URL for 'matrix-docker-ansible-deploy'.)
- deploy_branch			(Branch of this repository to use.)
- client_private_ssh_key 	(Location of private client key AWX will use.)
- client_private_ssh_key_password 	(Strong password for this private key.)
- vault_unlock_ssh_password:	(Strong password to vault the private_ssh_key_password.)
- client_public_ssh_key 	(Location of public client key AWX will use.)

If you will be using a backup server, also define:
- backup_server_enabled		('true' if using a backup server, otherwise 'false')
If 'false' you can skip these:
- backup_server_ip 		(IP address of the backup server.)
- backup_server_hostname 	(The hostname of the backup server.)
- backup_server_user 		(The username of the backup server.)
- backup_server_directory 	(The directory to backup to on the backup server.)
- backup_server_location:	(The location of the backup server.)
- backup_awx_encryption_passphrase 	(Strong password for the AWX borg backup.)
- backup_private_ssh_key	(Location of passwordless private backup key AWX will use.)
- backup_public_ssh_key		(Location of public backup key AWX will use.)
- vault_unlock_borg_passwords	(Strong password to vault the clients borg backup keys.)

If using the Mailgun relay define these values, if not then enter placeholder values (eg: 1234): 
- mg_sender_email_address	(The Mailgun email address. eg: "user@mail.example.org")
- mg_sender_domain		(The Mailgun email domain. eg: "mail.example.org"
- mg_relay_host_name		(The Mailgun relay host name. eg: "smtp.mailgun.org")
- mg_api_url			(The Mailgun API location. eg: "api.mailgun.net")
- mg_private_api_key		(The Mailgun private API key.)

Also add placeholder values to the following (eg: 1234), these won't be used:
- do_api_token 			(Your DigitalOcean API token/)
- do_spaces_access_key 		(Your DigitalOcean Spaces Access Key.)
- do_spaces_secret_key 		(Your DigitalOcean Spaces Secret Key.)
- do_image_master 		(eg: debian-10-x64)

Run the script:

`$ ansible-playbook -v -i ./inventory/hosts -t "setup" pre-setup.yml`


2) Run the AWX deployment script.
```
$ cd ..
$ wget https://github.com/ansible/awx/archive/17.1.0.tar.gz
$ tar -xf 17.1.0.tar.gz
$ cd ./awx-17.1.0/
```

Generate and record 3 strong passwords for the:
- secret_key
- pg_password
- admin_password (from above)

^ Edit these into ./installer/inventory, also add project_data_dir line and change host_port:
```
host_port=8080
#host_port_ssl=443
...
project_data_dir=/var/lib/awx/projects
```

Next comment out the first line and edit the awx_url into ./installer/inventory
```
#localhost ansible_connection=local ansible_python_interpreter="/usr/bin/env python3"
panel.example.org
```

Next, run the playbook to install the Ansible AWX with the following command:

`$ ansible-playbook -i ./installer/inventory ./installer/install.yml`


3) Post-setup, configures existing AWX system and adds community packages if 'configure-awx' tag set, also configures the AWX systems backup if 'setup-backup' and 'enable-backup' tag is included. Note that the backup machine will need SSH access to root.

Install prerequisite packages for ansible on the controller:

`$ ansible-galaxy collection install community.crypto`
`$ ansible-galaxy collection install --force awx.awx:17.1.0`

Run the script:

`$ ansible-playbook -v -i ./inventory/hosts -t "configure-awx" post-setup.yml`


4) Optionally, perform initial SSH handshake from AWX to backup server.

Manually SSH into the AWX tower, then manually SSH into the backup server:
`$ ssh {{ backup_server_hostname }}`

Note the command-line here is restricted, so you won't be able to do anything besides connnect.


5) Set base URL in AWX

Settings > Miscellaneous System Settings > Edit

Change 'Base URL of the Tower host' to your AWX systems URL.


