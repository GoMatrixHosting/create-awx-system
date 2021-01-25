
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

Next, comment out the following line to allow a local build:
```
#dockerhub_base=ansible
```

Copy in custom media logos:
```
$ cp ../create-awx-system/media/favicon.ico ./awx/ui/client/assets/favicon.ico
$ cp ../create-awx-system/media/logo-header.svg ./awx/ui/client/assets/logo-header.svg
$ cp ../create-awx-system/media/logo-login.svg ./awx/ui/client/assets/logo-login.svg
```

Edit the capital letters in 'PowerTools' out of the Dockerfile.j2:
```
$ sed -i 's/PowerTools/powertools/g' ./installer/roles/image_build/templates/Dockerfile.j2
```

Copy the playbook files to the target server.

Next, run the playbook to install the Ansible AWX with the following command:

`$ ansible-playbook -i ./installer/inventory ./installer/install.yml`


