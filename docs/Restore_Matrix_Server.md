
~~ Restore Matrix Server ~~

1) Locate the borg backups password. (This should be stored somewhere else!)

root@AWX-5-panel:~# cat /var/lib/awx/projects/clients/billy.bob/T-LD0RZ34UZ0I8/matrix_vars.yml | grep matrix_awx_backup_encryption_passphrase
matrix_awx_backup_encryption_passphrase: 7d1a32d698ab42c0523f4debe06e0c8d

2) Restore backup from borg repo:

pcadmin@kvm4-backupbox:~$ ls /mnt/backup-dir/Clients/absolutematrix.com/
config  data  hints.17  index.17  integrity.17  nonce  README
pcadmin@kvm4-backupbox:~$ mkdir /mnt/mfs/GMH-Backups/extracted/
pcadmin@kvm4-backupbox:~$ borg list /mnt/mfs/GMH-Backups/Clients/absolutematrix.com/
Enter passphrase for key /mnt/mfs/GMH-Backups/Clients/absolutematrix.com: 
...
absolutematrix-2021-03-02T12:43:48   Tue, 2021-03-02 20:43:53 [b96d30526180fe29ae5eafd5c883377869dcae9333af3e5ed8cbfeeeca954349]
pcadmin@kvm4-backupbox:~$ cd /mnt/mfs/GMH-Backups/extracted/
pcadmin@kvm4-backupbox:/mnt/mfs/GMH-Backups/extracted$ borg extract /mnt/mfs/GMH-Backups/Clients/absolutematrix.com/::absolutematrix-2021-03-02T12:43:48 chroot/export

3) Download extracted export to controller:

michael@gomatrixhosting:~/Documents$ scp -r pcadmin@kvm4-backupbox:/mnt/mfs/GMH-Backups/extracted/chroot ./
matrix.tar.gz                                              100% 6139KB   5.7MB/s   00:01
postgres_2021-03-02.sql.gz                                 100% 7496KB   6.4MB/s   00:01

4) Continue with the steps defined in [Import_Matrix_server.md in the docs/ directory](/docs/Import_Matrix_server.md).
