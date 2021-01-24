
~~ AWX System Backup && Restore ~~

1) Ensure a recent backup has executed properly:

root@AWX-old:~# docker exec -t awx_postgres pg_dump -U awx awx > /var/lib/awx/projects/awx-dump.sql; /usr/bin/borgmatic


2) Export backup from borg:

pcadmin@kvm4-backupbox:~$ ls /mnt/mfs/GMH-Backups/AWX/panel.topgunmatrix.com/
config  data  hints.74  index.74  integrity.74  nonce  README
pcadmin@kvm4-backupbox:~$ mkdir /mnt/mfs/GMH-Backups/AWX/extracted
pcadmin@kvm4-backupbox:~$ borg list /mnt/mfs/GMH-Backups/AWX/panel.topgunmatrix.com/
Enter passphrase for key /mnt/mfs/GMH-Backups/AWX/panel.topgunmatrix.com: 
...
AWX-3-panel-2021-01-24T03:49:44      Sun, 2021-01-24 11:49:47 [c48f8e4ee3f7e6feb361adc939623867b2abdec557aa1057d4c168042257f3fc]
pcadmin@kvm4-backupbox:~$ cd /mnt/mfs/GMH-Backups/AWX/extracted

pcadmin@kvm4-backupbox:/mnt/mfs/GMH-Backups/AWX/extracted$ borg extract /mnt/mfs/GMH-Backups/AWX/panel.topgunmatrix.com/::AWX-3-panel-2021-01-24T03:49:44 var/lib/awx/projects


3) Change DNS entry for AWX to new IP. (panel.example.org and monitor.example.org)


4) Re-create AWX setup on the new server:

Using the same vars.yml, follow the setup steps in Installation.md until the end of step 2.


5) Ensure old backup repo is deleted/moved:

pcadmin@kvm4-backupbox:/mnt/mfs/GMH-Backups/AWX$ mv ./panel.topgunmatrix.com ./panel.topgunmatrix.com-old


6) Check that AWX system is up and running.


7) Run post-setup.yml while skipping the 'enable-backup' and 'configure-awx' tag:

$ ansible-playbook -v -i ./inventory/hosts -t "setup-radius,setup-swatchdog,setup-backup" --skip-tags="configure-awx,enable-backup" post-setup.yml


8) Restore /var/lib/awx/projects to new AWX system:

root@AWX-3-panel:~# apt install rsync
root@AWX-3-panel:~# rm -r /var/lib/awx/projects/*

chatoasis@debian:/media/chatoasis/Nitrokey Encrypt/create-awx-system$ rsync -av /mnt/mfs/GMH-Backups/extracted/var/lib/awx/projects root@panel.topgunmatrix.com:/var/lib/awx/

root@AWX-3-panel:~# chown -R root:root /var/lib/awx/projects


9) Run import on AWX tower:




