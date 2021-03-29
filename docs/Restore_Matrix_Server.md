
~~ Restore Matrix Server ~~

1) Locate the borg backups password.

root@AWX7-panel:~# cat /var/lib/awx/projects/backups/farmloop.xyz-borg_backup.yml 
matrix_awx_backup_encryption_passphrase: 75262145df78f618fae141fb32641d19

2) Restore backup from borg repo:

backup_user@backup_server:~$ ls /mnt/backup-dir/Clients/absolutematrix.com/
config  data  hints.17  index.17  integrity.17  nonce  README
backup_user@backup_server:~$ mkdir /mnt/backup-dir/extracted/
backup_user@backup_server:~$ borg list /mnt/backup-dir/Clients/absolutematrix.com/
Enter passphrase for key /mnt/mfs/GMH-Backups/Clients/absolutematrix.com: 
...
absolutematrix-2021-03-02T12:43:48   Tue, 2021-03-02 20:43:53 [b96d30526180fe29ae5eafd5c883377869dcae9333af3e5ed8cbfeeeca954349]
backup_user@backup_server:~$ cd /mnt/backup-dir/extracted/
backup_user@backup_server:/mnt/backup-dir/extracted$ borg extract /mnt/backup-dir/Clients/absolutematrix.com/::absolutematrix-2021-03-02T12:43:48 chroot/export

3) Download extracted export to controller:

michael@gomatrixhosting:~/Documents$ scp -r backup_user@backup_server:/mnt/backup-dir/extracted/chroot ./
matrix.tar.gz                                              100% 6139KB   5.7MB/s   00:01
postgres_2021-03-02.sql.gz                                 100% 7496KB   6.4MB/s   00:01

4) Continue with the steps defined in [Import_Matrix_server.md in the docs/ directory](/docs/Import_Matrix_server.md).
