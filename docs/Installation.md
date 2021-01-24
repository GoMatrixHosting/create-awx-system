# GoMatrixHosting AWX Setup - Installation Instructions


# Create a server

Create a Debian 10 server and setup SSH access to root user.
```
$ ssh root@panel.example.org
$ exit
```

# Setup DNS entry for it:

Map 2 A records for panel.example.org and monitor.example.org to the servers IP.


# Installation

Installation is broken up into 6 stages:

1) Pre-setup, setup before the awx playbook is run, installs Docker and sets up TLS proxy for AWX, optionally website hooks and grafana are also setup.

`$ git clone https://gitlab.com/GoMatrixHosting/create-awx-system.git`

Install prerequisite packages for ansible on the controller:

`$ ansible-galaxy collection install community.grafana`

Edit host into: ./inventory/hosts

Create folder for host at: ./inventory/host_vars/panel.example.org/

Record these variables to ./inventory/host_vars/panel.example.org/vars.yml:
- org_name 			(The name of your organisation.)
- awx_url 			(The URL for AWX.)
- grafana_url 			(The URL for Grafana.)
- certbot_email 		(The organisations email.)
- admin_password 		(Strong password for the AWX admin user.)
- private_ssh_key 		(Location of private key AWX will use.)
- private_ssh_key_password 	(Strong password for this private key.)
- public_ssh_key 		(Location of public key AWX will use.)
If you wish to configure a backup server, also define:
- backup_server_ip 		(IP address of the backup server.)
- backup_server_hostname 	(The hostname of the backup server.)
- backup_server_user 		(The username of the backup server.)
- backup_server_directory 	(The directory to backup to on the backup server.)
- backup_encryption_passphrase 	(Strong password for the AWX borg backup.)
If you will be using this setup commercially, also define:
- do_api_token 			(Your DigitalOcean API token/)
- do_spaces_access_key 		(Your DigitalOcean Spaces Access Key.)
- do_spaces_secret_key 		(Your DigitalOcean Spaces Secret Key.)
- do_image_master 		(eg: debian-10-x64)

Run the script:

`$ ansible-playbook -v -i ./inventory/hosts -t "setup,setup-monitor,setup-webhooks" pre-setup.yml`


2) Run the AWX deployment script.
```
$ cd ..
$ wget https://github.com/ansible/awx/archive/15.0.1.tar.gz
$ tar -xf 15.0.1.tar.gz
$ cd ./awx-15.0.1/
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
`$ ansible-galaxy collection install awx.awx`

Run the script:

`$ ansible-playbook -v -i ./inventory/hosts -t "configure-awx,setup-radius,setup-swatchdog,setup-backup,enable-backup" post-setup.yml`


4) Perform initial SSH handshake from AWX to backup server.

Manually SSH into the AWX tower, then manually SSH into the backup server:
`$ ssh {{ backup_server_hostname }}`

Note the command-line here is restricted, so you won't be able to do anything besides connnect.


5) Connect FreeRADIUS server to AWX

In the 'Authentication' > 'Radius' page:

RADIUS SERVER:	172.17.0.1
RADIUS PORT:	1812
RADIUS SECRET:	"{{ radius_secret }}"


6) Setup grafana.

The Grafana needs extra configuration to work, follow the [Grafana.md in the docs/ directory](docs/Grafana.md).

