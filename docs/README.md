# GoMatrixHosting AWX Setup - Installation Instructions


# Setup DNS entry for it:

Map 2 A records for panel.example.org and monitor.example.org to the servers IP.


# Installation

Installation is broken up into 3 stages:

1) Pre-setup, setup before the awx playbook is run, installs Docker and sets up TLS proxy for AWX, optionally website hooks and graphana are also setup.

Record these variables:
- awx_url (eg: panel.example.org)
- graphana_url (eg: monitor.example.org)
- certbot_email (eg: myemail@protonmail.com)
- admin_password (For the AWX admin user, eg: NAMQvAHm6rFG6d2oxx2a)

`$ ansible-playbook -i ./inventory/hosts -t "setup-monitor,setup-webhooks" pre_setup.yml`


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

Next, run the playbook to install the Ansible AWX with the following command:

`$ ansible-playbook -i ./awx/installer/inventory install.yml`


3) Post-setup, configures existing AWX system.

~ Not yet made, basically these steps:

Edit default org to ‘ChatOasis’.

Add ‘admin’ user to ‘ChatOasis’ org.

Add ‘ChatOasis Ansible Create Organisation and Server’ project to this org.

Add ‘ChatOasis Ansible Delete Organisation and Servers’ project to this org.

Add ‘ChatOasis testing SSH’ credential to this org. ‘Machine’ type with actual SSH key.

Add ‘ChatOasis Servers’ inventory. Add ‘dummyvalue.com’ to it.

Add ‘00 - Create Organisation and Server’ job template. Use above objects. Add extra variables:

matrix_domain: perthchat.news
do_droplet_region: nyc1
plan_size: small
client_organisation: Perthchat News
client_email: perthchat@protonmail.com
client_password: dummypassword9846

Add ‘01 - Delete Organisation and Servers’ job template. Use above objects. Add extra variables:

matrix_domain: testtags.org
client_organisation: Test-Tags
