# GoMatrixHosting AWX Setup - Installation Instructions


# Setup DNS entry for it:

Map A record for panel.example.org to the servers IP.


# Installation

Installation is broken up into 3 stages:

1) Pre-setup, setup before the awx playbook is run, installs Docker and sets up TLS proxy for AWX, optionally website hooks and graphana are also setup.

Record these variables:
- awx_url (panel.topgunmatrix.com)
- graphana_url (monitor.topgunmatrix.com)
- certbot_email (myemail@protonmail.com)

`$ ansible-playbook -i inventory/hosts pre_setup.yml`


2) Run the AWX deployment script.

`$ git clone --depth 50 https://github.com/ansible/awx.git`

Generate and record 3 strong passwords for the:
- secret_key
- pg_password
- admin_password

^ Edit these into /awx/installer/inventory, also add project_data_dir line and change host_port:
```
project_data_dir=/var/lib/awx/projects
host_port=8080
#host_port_ssl=443
```

Next, run the playbook to install the Ansible AWX with the following command:

`$ ansible-playbook -i /awx/installer/inventory install.yml`


3) Post-setup, configures existing AWX system.

~ Not yet made, basically these steps:

