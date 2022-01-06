# GoMatrixHosting AWX Setup - Minimal Installation Instructions

How to install this AWX setup without a front-end wordpress site, digitalocean service, graphana monitor, or backup server.

# Create a server

Create a Debian 10/11 server with at least 4GB or RAM and setup SSH access to root user.
```
$ ssh root@panel.example.org
$ exit
```

# Setup DNS entry for it:

Map an A/AAAA record for panel.example.org to the servers IP.


# Installation

1) Pre-setup, setup before the awx playbook is run, installs Docker and sets up TLS proxy for AWX, optionally website hooks and grafana are also setup.

`$ git clone https://gitlab.com/GoMatrixHosting/create-awx-system.git`

Install prerequisite packages for ansible on the controller:

`$ ansible-galaxy collection install community.grafana`

Edit host into: ./inventory/hosts

Create folder for host at: ./inventory/host_vars/panel.example.org/

Record these variables to ./inventory/host_vars/panel.example.org/vars.yml:
- org_name 			(The name of your organisation.)
- hosting_url			(The URL of your organisation.)
- awx_url 			(The URL for AWX.)
- certbot_email 		(The organisations email.)
- secret_key			(Strong password for the AWX secrets.)
- pg_password			(Strong password for the AWX database.)
- admin_password 		(Strong password for the AWX admin user.)
- delete_subscription_hours_delay	(The number of hours to delay the subscription deletion.)
- update_schedule_start		(The start time for scheduled client updates in 'YYYYMMDDTHHMMSS' format, for example '20211030T080000' which means the 30th of October 2021 at 8AM.)
- update_schedule_frequency	(The time period for scheduled client updates, options are 'MINUTELY', 'HOURLY', 'DAILY', 'WEEKLY','MONTHLY')
- update_schedule_interval	(The number of minutes/hours/days/weeks/months to schedule client updates to.)
- create_delete_source		(Repository URL for 'Ansible Create Delete Subscription Membership'.)
- create_delete_branch		(Branch of this repository to use.)
- provision_source		(Repository URL for 'Ansible Provision'.)
- provision_branch		(Branch of this repository to use.)
- deploy_source			(Repository URL for 'matrix-docker-ansible-deploy'.)
- deploy_branch			(Branch of this repository to use.)
- client_public_ssh_key 	(Location of public client key AWX will use.)
- client_private_ssh_key 	(Location of private client key AWX will use.)
- client_private_ssh_key_password 	(Strong password for this private key.)
- vault_unlock_ssh_password:	(Strong password to vault the private_ssh_key_password.)

Since you won't be using a backup server, also define:
- backup_server_enabled		('false')

If using the Mailgun relay define these values: 
- mg_sender_email_address	(The Mailgun email address. eg: "user@mail.example.org")
- mg_sender_domain		(The Mailgun email domain. eg: "mail.example.org"
- mg_relay_host_name		(The Mailgun relay host name. eg: "smtp.mailgun.org")
- mg_api_url			(The Mailgun API location. eg: "api.mailgun.net")
- mg_private_api_key		(The Mailgun private API key.)

If using DigitalOcean define these values:
- do_api_token 			(Your DigitalOcean API token/)
- do_spaces_access_key 		(Your DigitalOcean Spaces Access Key.)
- do_spaces_secret_key 		(Your DigitalOcean Spaces Secret Key.)
- do_image_master 		(eg: debian-10-x64)

Run the script:

`$ ansible-playbook -v -i ./inventory/hosts -t "setup" pre_setup.yml`


2) Run the AWX deployment script.
```
$ cd ..
$ wget https://github.com/ansible/awx/archive/17.1.0.tar.gz
$ tar -xf 17.1.0.tar.gz
$ cd ./awx-17.1.0/
```

From the above variables, copy the following:
- secret_key
- pg_password
- admin_password

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

`$ ansible-playbook -v -i ./inventory/hosts -t "generate-token,configure-awx" post_setup.yml`


4) Set base URL in AWX

Settings > Miscellaneous System Settings > Edit

Change 'Base URL of the Tower host' to your AWX systems URL.


