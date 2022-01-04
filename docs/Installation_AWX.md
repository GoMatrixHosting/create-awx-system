# GoMatrixHosting AWX Setup - Installation Instructions


# Create a server

Create a Debian 10/11 server and setup SSH access to root user.
```
$ ssh root@panel.example.org
$ exit
```

# Setup DNS entry for it:

Create 2 A/AAAA records for panel.example.org and monitor.example.org pointing to the AWX servers IP.


# Installation

Installation is broken up into 8 stages:

1) Optionally, create a backup server. You should be able to access root using a IP that the AWX server can reach and the 'client_private_ssh_key', it should also contain a depriviledged user 'backup_server_user' and backup location 'backup_server_location'. Collect its SSH fingerprint and save it to 'backup_server_ssh_fingerprint', to collect it run this command:

$ ssh-keyscan -t ed25519 {{ backup_server_ip }} 2>/dev/null
255.150.40.99 ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOdNgn7zqlpWIsiTV91QLEtRnXH18uMC27zVJYHsql/D

Create a A/AAAA record for backup.example.org pointing to the backup servers IP.

Install prometheus-node-exporter and export port 9100 on the backup server.


2) Pre-setup, setup before the awx playbook is run, installs Docker and sets up TLS proxy for AWX, optionally website hooks and grafana are also setup.

`$ git clone https://gitlab.com/GoMatrixHosting/create-awx-system.git`

Install prerequisite packages for ansible on the controller:

`$ ansible-galaxy collection install community.grafana`

Edit host into: ./inventory/hosts

Create folder for host at: ./inventory/host_vars/panel.example.org/

Record these variables to ./inventory/host_vars/panel.example.org/vars.yml:
- org_name 			(The name of your organisation.)
- hosting_url			(The URL of your organisation.)
- awx_url 			(The URL for AWX.)
- grafana_url 			(The URL for Grafana.)
- certbot_email 		(The organisations email.)
- grafana_admin_password	(Graphana admin users password.)
- prometheus_retention_period	(Number of days to retain the monitoring data.)
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

If you will be using the Mailgun relay, define:
- mg_sender_email_address	(The Mailgun email address. eg: "user@mail.example.org")
- mg_sender_domain		(The Mailgun email domain. eg: "mail.example.org"
- mg_relay_host_name		(The Mailgun relay host name. eg: "smtp.mailgun.org")
- mg_api_url			(The Mailgun API location. eg: "api.mailgun.net")
- mg_private_api_key		(The Mailgun private API key.)

If you will be using a backup server, define:
- backup_server_enabled		('true' if using a backup server, otherwise 'false')
- backup_server_ip 		(IP address of the backup server.)
- backup_server_hostname 	(The hostname of the backup server.)
- backup_server_user 		(The username of the backup server.)
- backup_server_directory 	(The directory to backup to on the backup server.)
- backup_server_location:	(The location of the backup server.)
- backup_awx_encryption_passphrase 	(Strong password for the AWX borg backup.)
- backup_server_ssh_fingerprint (The host SSH fingerprint of your backup server.)
- backup_schedule_start		(The start time for scheduled client backups in 'YYYYMMDDTHHMMSS' format, for example '20211030T080000' which means the 30th of October 2021 at 8AM.)
- backup_schedule_frequency	(The time period for schedules client backups, options are 'MINUTELY', 'HOURLY', 'DAILY', 'WEEKLY','MONTHLY')
- backup_schedule_interval	(The number of minutes/hours/days/weeks/months to schedule client backups to.)

If you want to spawn Matrix servers using DigitalOcean, define:
- do_api_token 			(Your DigitalOcean API token/)
- do_spaces_access_key 		(Your DigitalOcean Spaces Access Key.)
- do_spaces_secret_key 		(Your DigitalOcean Spaces Secret Key.)
- do_image_master 		(eg: debian-10-x64)

If you will be using this setup commercially, define:
- radius_secret			(Strong password for authenticating AWX against FreeRadius.)
- oauth_client_id		(client_id from WP Oauth Server WordPress plugin.)
- oauth_client_secret		(client_secret from WP Oauth Server WordPress plugin.)
- wp_url			(The URL of the front-end WordPress site.)
- wp_username			(The front-end WordPress username you SSH into.)

Run the script:
`$ ansible-playbook -v -i ./inventory/hosts -t "setup,setup-monitor" pre_setup.yml`


3) Run the AWX deployment script.
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


4) Post-setup, configures existing AWX system and adds community packages if 'configure-awx' tag set, also configures the AWX systems backup if 'setup-backup' and 'enable-backup' tag is included. Note that the backup machine will need SSH access to root.

Install prerequisite packages for ansible on the controller:

`$ ansible-galaxy collection install community.crypto`
`$ ansible-galaxy collection install --force awx.awx:17.1.0`

Run the script:

`$ ansible-playbook -v -i ./inventory/hosts -t "generate-token,configure-awx,setup-webhooks,setup-radius,setup-swatchdog,setup-backup,enable-backup" post_setup.yml`


5) Perform initial SSH handshake from AWX to backup server.

Manually SSH into the AWX tower, then manually SSH into the backup server:
`$ ssh {{ backup_server_hostname }}`

Note the command-line here is restricted, so you won't be able to do anything besides connnect.


6) Connect AWX to FreeRADIUS server

In the 'Authentication' > 'Radius' page:

RADIUS SERVER:	Public IP of the AWX server.
RADIUS PORT:	1812
RADIUS SECRET:	"{{ radius_secret }}"


7) Set base URL in AWX

Settings > Miscellaneous System Settings > Edit

Change 'Base URL of the Tower host' to your AWX systems URL.


8) Setup grafana.

The Grafana needs extra configuration to work, follow the [Grafana.md in the docs/ directory](docs/Grafana.md).

