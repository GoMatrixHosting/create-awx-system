# GoMatrixHosting AWX Setup - Installation Instructions


# Create a server

Create a Debian 10 server and setup SSH access to root user.

'$ sudo apt install python3-apt-dbg python3-apt python-apt-doc python-apt-common'


# Setup DNS entry for it:

Map 2 A records for panel.example.org and monitor.example.org to the servers IP.


# Installation

Installation is broken up into 4 stages:

1) Pre-setup, setup before the awx playbook is run, installs Docker and sets up TLS proxy for AWX, optionally website hooks and grafana are also setup.

`$ git clone https://gitlab.com/GoMatrixHosting/create-awx-system.git`

Install prerequisite packages for ansible on the controller:

`$ ansible-galaxy collection install community.grafana`

Edit host into: ./inventory/hosts

Create folder for host at: ./inventory/host_vars/panel.example.org/

Record these variables to ./inventory/host_vars/panel.example.org/vars.yml:
- org_name (The name of your organisation, eg: GoMatrixHosting)
- awx_url (The URL for AWX, eg: panel.example.org)
- grafana_url (The URL for Grafana, eg: monitor.example.org)
- certbot_email (eg: myemail@protonmail.com)
- admin_password (For the AWX admin user, eg: NAMQvAHm6rFG6d2oxx2a)
- private_ssh_key (Location of private key AWX will use.)
- private_ssh_key_password (The password to this private key.)
- public_ssh_key (Location of public key AWX will use.)
If you will be using this setup commercially, also define:
- do_api_token (Your DigitalOcean API token/)
- do_spaces_access_key (Your DigitalOcean Spaces Access Key.)
- do_spaces_secret_key (Your DigitalOcean Spaces Secret Key.)
- do_image_master (eg: debian-10-x64)

Run the script:

`$ ansible-playbook -v -i ./inventory/hosts -t "setup,setup-monitor,setup-webhooks" pre-setup.yml`


2) Run the AWX deployment script.

`$ git clone --depth 50 https://github.com/ansible/awx.git`

Generate and record 3 strong passwords for the:
- secret_key
- pg_password
- admin_password (from above)

^ Edit these into /awx/installer/inventory, also add project_data_dir line and change host_port:
```
project_data_dir=/var/lib/awx/projects
host_port=8080
#host_port_ssl=443
```

Next comment out the first line and edit the awx_url into ./installer/inventory
```
#localhost ansible_connection=local ansible_python_interpreter="/usr/bin/env python3"
panel.example.org
```

Next, run the playbook to install the Ansible AWX with the following command:

`$ ansible-playbook -i ./awx/installer/inventory install.yml`


3) Post-setup, configures existing AWX system and adds community packages.

Run the script:

`$ ansible-playbook -v -i ./inventory/hosts post-setup.yml`


4) Setup grafana.

The Grafana needs extra configuration to work, follow the [Grafana.md in the docs/ directory](docs/Grafana.md).
