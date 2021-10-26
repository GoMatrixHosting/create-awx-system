
1-2) Complete steps 1 and 2 from /docs/Installation_AWX.md.

3) Configure and run the AWX installation script.
```
$ git clone https://github.com/ansible/awx.git
$ cd ./awx
$ git checkout tags/17.1.0
```

Generate and record 3 strong passwords for the:
- secret_key
- pg_password
- admin_password (from step 2)

^ Edit these into ./awx/installer/inventory, also uncomment the project_data_dir line and change the host_port and host_port_ssl values:
```
host_port=8080
#host_port_ssl=443
...
project_data_dir=/var/lib/awx/projects
```

Next, comment out the following line to allow a local build:
```
#dockerhub_base=ansible
```

Copy in your custom media logos:
```
$ cp ./create-awx-system/media/favicon.ico ./awx/awx/static/favicon.ico
$ cp ./create-awx-system/media/logo-header.svg ./awx/awx/ui_next/public/static/media/logo-header.svg
$ cp ./create-awx-system/media/logo-login.svg ./awx/awx/ui_next/public/static/media/logo-login.svg
```

4) Copy the playbook files to the target server:
```
$ rsync -av ./awx panel.example.org:/root/
```

5) Next, connect to your AWX server and run the playbook to install the AWX:
```
# echo 'deb http://deb.debian.org/debian buster-backports main' >> /etc/apt/sources.list
# sudo apt update && sudo apt -t buster-backports install ansible
# ansible-galaxy collection install community.docker
# cd /root/awx
# ansible-playbook -i ./installer/inventory ./installer/install.yml
```

6) Modify the python package Radius uses, and increase its timeout value:
```
# docker exec -it awx_web /bin/bash
bash-4.4# vi /var/lib/awx/venv/awx/lib/python3.6/site-packages/pyrad/client.py && rm -r /var/lib/awx/venv/awx/lib/python3.6/site-packages/pyrad/__pycache__
```

Change timeout value to 30:
```
        self.timeout = 30
```

7) Continue from step 4 of /docs/Installation_AWX.md.

