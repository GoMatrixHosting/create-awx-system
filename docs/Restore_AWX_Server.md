
~~ Restore AWX Server ~~

1) Ensure a recent backup has executed properly:

root@AWX-old:~# docker exec -t awx_postgres pg_dump -U awx awx > /var/lib/awx/projects/awx-dump.sql; /usr/bin/borgmatic


2) Export backup from borg:

pcadmin@backup-server:~$ ls /mnt/backup-dir/AWX/panel.example.org/
config  data  hints.74  index.74  integrity.74  nonce  README
pcadmin@backup-server:~$ mkdir /mnt/backup-dir/AWX/extracted
pcadmin@backup-server:~$ borg list /mnt/backup-dir/AWX/panel.example.org/
Enter passphrase for key /mnt/backup-dir/AWX/panel.example.org: 
...
AWX-3-panel-2021-01-24T03:49:44      Sun, 2021-01-24 11:49:47 [c48f8e4ee3f7e6feb361adc939623867b2abdec557aa1057d4c168042257f3fc]
pcadmin@backup-server:~$ cd /mnt/backup-dir/AWX/extracted

pcadmin@backup-server:/mnt/backup-dir/AWX/extracted$ borg extract /mnt/backup-dir/AWX/panel.example.org/::AWX-3-panel-2021-01-24T03:49:44 var/lib/awx/projects


3) Change DNS entry for AWX to new IP. (panel.example.org and monitor.example.org)


4) Re-create AWX setup on the new server:

Using the same vars.yml, follow the setup steps in Installation.md until the end of step 3.


5) Ensure old backup repo is deleted/moved:

pcadmin@backup-server:/mnt/backup-dir/AWX$ mv ./panel.example.org ./panel.example.org-old


6) Check that AWX system is up and running.


7) Run post-setup.yml while skipping the 'enable-backup' and 'configure-awx' tag:

$ ansible-playbook -v -i ./inventory/hosts -t "setup-radius,setup-swatchdog,setup-backup" post-setup.yml


8) Restore /var/lib/awx/projects to new AWX system with correct permissions:

root@AWX-new:~# docker stop awx_task
awx_task
root@AWX-new:~# docker stop awx_web
awx_web
root@AWX-new:~# apt install rsync
root@AWX-new:~# rm -r /var/lib/awx/projects/*

$ rsync -av backup-server:/mnt/backup-dir/AWX/extracted/var/lib/awx/projects ./
$ rsync -av ./projects panel.example.org:/var/lib/awx/

root@AWX-new:~# chown -R root:root /var/lib/awx/projects
root@AWX-new:~# chmod 755 /var
root@AWX-new:~# chmod 755 /var/lib
root@AWX-new:~# chmod 755 /var/lib/awx
root@AWX-new:~# chmod 755 /var/lib/awx/projects
root@AWX-new:~# chmod 711 /var/lib/awx/projects/clients
root@AWX-new:~# chmod 711 /var/lib/awx/projects/clients/*
root@AWX-new:~# chmod 700 /var/lib/awx/projects/clients/*/*
root@AWX-new:~# chmod 660 /var/lib/awx/projects/clients/client-list
root@AWX-new:~# chown root:webhook /var/lib/awx/projects/clients/client-list
root@AWX-new:~# chmod 660 /var/lib/awx/projects/clients/*/organisation.yml
root@AWX-new:~# chown root:webhook /var/lib/awx/projects/clients/*/organisation.yml
root@AWX-new:~# chmod 600 /var/lib/awx/projects/clients/*/*/*


9) Run import on AWX tower:

root@AWX-new:~# cp /var/lib/awx/projects/awx-dump.sql /root/.awx/pgdocker/12/data/
root@AWX-new:~# docker exec -it awx_postgres /bin/bash
root@ce48e2584014:/# dropdb -U awx awx
root@ce48e2584014:/# createdb -U awx awx
root@ce48e2584014:/# psql -U awx awx < /var/lib/postgresql/data/awx-dump.sql
root@ce48e2584014:/# exit
root@AWX-new:~# docker start awx_task
awx_task
root@AWX-new:~# docker start awx_web
awx_web


10) Check if the data has been imported properly:

Try login as a user account, looks good? :)


11) Activate backup and complete installation:

$ ansible-playbook -v -i ./inventory/hosts -t "enable-backup" post-setup.yml

*Follow the rest of Installation.md from step 5.

