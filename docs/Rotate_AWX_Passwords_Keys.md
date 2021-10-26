
# Rotating AWX passwords and SSH keys

1) Update the admin_password and grafana_admin_password variables in the create-awx-system vars.yml file.
```
$ nano ./inventory/host_vars/panel.example.org/vars.yml
```

2) In the AWX repository update the admin_password variable in the ./installer/inventory file:
```
$ ssh panel.example.org
Linux AWX7-panel 4.19.0-16-cloud-amd64 #1 SMP Debian 4.19.181-1 (2021-03-19) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Wed Sep  8 12:18:00 2021 from 180.150.92.58
root@AWX7-panel:~# cd /root/awx
root@AWX7-panel:~/awx# nano ./installer/inventory
```


3) Change the admin password to the new value in the AWX GUI.


4) Generate new SSH keys for the AWX server, AWX > Client and Client > Backup Server (passwordless):

$ ssh-keygen -o -a 100 -t ed25519 -f ~/.ssh/awxtower3_ed25519 -C "AWX server"
Generating public/private ed25519 key pair.
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/username/.ssh/awxtower3_ed25519
Your public key has been saved in /home/username/.ssh/awxtower3_ed25519.pub

$ ssh-keygen -o -a 100 -t ed25519 -f ~/.ssh/matrixtesting3_ed25519 -C "AWX > Client SSH key"
Generating public/private ed25519 key pair.
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/username/.ssh/matrixtesting3_ed25519
Your public key has been saved in /home/username/.ssh/matrixtesting3_ed25519.pub


5) Update the SSH key for the AWX system and edit out the previous public SSH key from /root/.ssh/authorized_keys:
```
$ cat ~/.ssh/awxtower3_ed25519.pub
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDNRZ5WzK+pUUlx+miN0PxPiel0XaR8JUe0QwgY9lHV9 AWX server
$ ssh panel.example.org
...
root@panel:~# cp /root/.ssh/authorized_keys /root/.ssh/authorized_keys.backup \
&& truncate -s 0 /root/.ssh/authorized_keys \
&& echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDNRZ5WzK+pUUlx+miN0PxPiel0XaR8JUe0QwgY9lHV9 AWX server" >> /root/.ssh/authorized_keys
```


6) Update your local SSH config with the new AWX server SSH key:
```
$ nano ~/.ssh/config
...
Host panel.example.org
    HostName 167.172.128.69
    User root
    Port 22
    IdentityFile ~/.ssh/awxtower3_ed25519
```


7) Re-test SSH access on the AWX system:
```
$ ssh panel.example.org
```


8) Update the SSH key for the backup server and edit out the previous public SSH key from /root/.ssh/authorized_keys:
```
$ cat ~/.ssh/matrixtesting3_ed25519.pub
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGaL/Kpvw/ItlSg1xqIZxeZiHoSn7tVkmQvI+MdL/+Ch AWX > Client SSH key
$ ssh backup.example.org
...
root@backup:~# cp /root/.ssh/authorized_keys /root/.ssh/authorized_keys.backup \
&& truncate -s 0 /root/.ssh/authorized_keys \
&& echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGaL/Kpvw/ItlSg1xqIZxeZiHoSn7tVkmQvI+MdL/+Ch AWX > Client SSH key" >> /root/.ssh/authorized_keys
```


9) Update your local SSH config for the backup server with the new AWX > Client SSH key:
```
$ nano ~/.ssh/config
...
Host backup.example.org
    HostName 167.172.128.69
    User root
    Port 22
    IdentityFile ~/.ssh/matrixtesting3_ed25519
```


10) Re-test SSH access on the AWX system:
```
$ ssh backup.example.org
```


11) Set new values for the following in the create-awx-system vars.yml file:
```
client_private_ssh_key: /key/location/matrixtesting3_ed25519
client_public_ssh_key: /key/location/matrixtesting3_ed25519.pub
client_private_ssh_key_password: << strong-password >>
vault_unlock_ssh_password: << strong-password >>
```


12) Delete the existing borg backup key from the AWX server:
```
$ rm /root/.ssh/borg_backup_ed25519
$ rm /root/.ssh/borg_backup_ed25519.pub
```


13) Re-install the AWX system, see [Installation_AWX.md](https://gitlab.com/GoMatrixHosting/create-awx-system/-/blob/master/docs/Installation_AWX.md). 


14) Add the new client public key to your [DigitalOcean account settings](https://cloud.digitalocean.com/account/security).


15) Run every '0 - XXX - Provision Wireguard Server' job but change the following extra variable:
```
"update_ssh_key": "False"
```


16) Run the '00 - Rotate SSH Keys' job as the AWX admin.


17) Delete existing client backup ssh keys of every server from the AWX server:
```
$ rm /var/lib/awx/projects/clients/*/*/borg_backup_ed25519
$ rm /var/lib/awx/projects/clients/*/*/borg_backup_ed25519.pub
```


18) Run the '00 - Reprovision All Servers' job template.


19) Update the public SSH key on the front-end website for on-premises users.
