
~~ Recover Matrix Server ~~

A guide on how to recover a client's server.

1) Locate the borg backups password.

root@AWX7-panel:~# cat /var/lib/awx/projects/backups/stevesubway.xyz-borg_backup.yml 
awx_backup_encryption_passphrase: 0ba70e6786d0acc54c116c68a5a73d2c


2) Restore backup of /matrix from borg repo:

backup_user@backup_server:~$ ls /mnt/backup-dir/Clients/stevesubway.xyz/matrix/
config  data  hints.17  index.17  integrity.17  nonce  README
backup_user@backup_server:~$ borg list /mnt/backup-dir/Clients/stevesubway.xyz/matrix/
Enter passphrase for key /mnt/mfs/GMH-Backups/Clients/stevesubway.xyz/matrix: 
...
stevesubway-2021-06-12T06:32:44      Sat, 2021-06-12 14:32:45 [500b3fdee79eeb7b6c087c062335260496ca83e2eb5b2d84854892b399263d54]
backup_user@backup_server:~$ mkdir /mnt/backup-dir/Extracted/
backup_user@backup_server:~$ cd /mnt/backup-dir/Extracted/
backup_user@backup_server:/mnt/backup-dir/extracted$ borg extract /mnt/backup-dir/Clients/stevesubway.xyz/matrix/::stevesubway-2021-06-12T06:32:44


3) Restore backup of database from borg repo:

backup_user@backup_server:~$ ls /mnt/backup-dir/Clients/stevesubway.xyz/database/
config	data  hints.5  index.5	integrity.5  nonce  README
backup_user@backup_server:~$ borg list /mnt/backup-dir/Clients/Clients/stevesubway.xyz/database/
Enter passphrase for key /mnt/mfs/GMH-Backups/Clients/stevesubway.xyz/database: 
...
stevesubway-2021-06-12T06:32:59      Sat, 2021-06-12 14:33:01 [128f2393a58b0223d624a47a81b891d564993246ff200e6379723749e88da781]
backup_user@backup_server:~$ cd /mnt/backup-dir/extracted/
backup_user@backup_server:/mnt/backup-dir/extracted$ borg extract /mnt/backup-dir/Clients/absolutematrix.com/::absolutematrix-2021-03-02T12:43:48


4) Download extracted export to controller:

user@localhost:~/Documents$ rsync -av backup_server:/mnt/backup-dir/Extracted/ ./


5) Extract variables needed to re-create subscription:

On controller, extract matrix.tar.gz, examine /matrix/awx/organisation.yml and /matrix/awx/matrix_awx.yml and /matrix/awx/server_vars.yml and /matrix/awx/extra_vars.json, copy:

- client_email: "bobfett@protonmail.com"		[/matrix/awx/organisation.yml]
- client_first_name: "Bob"				[/matrix/awx/organisation.yml]
- client_last_name: "Fett"				[/matrix/awx/organisation.yml]
- matrix_domain: fishbole.xyz				[/matrix/awx/matrix_vars.yml]
- matrix_server_fqn_element: element.fishbole.xyz	[/matrix/awx/matrix_vars.yml]
- matrix_nginx_proxy_base_domain_serving_enabled: true	[/matrix/awx/matrix_vars.yml]
- subscription_type: digitalocean			[/matrix/awx/server_vars.yml]
- plan_title: Medium DigitalOcean Server		[/matrix/awx/extra_vars.json]
- subscription_id: I-CREUS74S6969			[/matrix/awx/extra_vars.json]
- member_id: 31						[/matrix/awx/extra_vars.json]

As well as:

- do_droplet_region: tor1				[/matrix/awx/server_vars.yml]
OR
- server_ipv4: 134.209.44.206				[/matrix/awx/server_vars.yml]
- server_ipv6: 2604:a880:800:c1::181:7001		[/matrix/awx/server_vars.yml]


6) Observe 'subscription_id' in server_vars.yml, if it's a MemberPress subscription (Starts with sub_) launch '00 - Ansible Create MP Subscription' with the above variables, otherwise if it's a manual subscription (Starts with T-) launch '00 - Ansible Create Manual Subscription'.


7) Ensure the previous backup has been moved:

backup_user@backup_server:~$ mv /mnt/backup-dir/Clients/fishbole.xyz/ /mnt/backup-dir/Clients/fishbole.xyz-old/


8) Remove the 'imposter-check' tag from 'Provision a New Server', then run the template with these survey answers:

SET BASE DOMAIN - matrix_domain

BASE DOMAIN USED - If matrix_nginx_proxy_base_domain_serving_enabled: true, then select 'false', otherwise select 'true'. 

SET ELEMENT SUBDOMAIN - Copy only the subdomain from matrix_server_fqn_element, for example only 'element' out of element.gnuperth.org.

SELECT REGION - Figure it out from the do_droplet_region. (Or a different one if you're trying to migrate it)

OR

SERVER IPV4/SERVER IPV6 - Enter the IPs for the new on-premises server. 


9) Note the new subscription_id and member_id. Load matrix_vars.yml from the restored backup into the new AWX subsciption folder:

~/Documents$ scp ./matrix/awx/matrix_vars.yml panel.topgunmatrix.com:/var/lib/awx/projects/clients/31/T-FKFAMCCR7CHX/
matrix_vars.yml                               100% 3840    13.1KB/s   00:00 


10) Clear known_hosts entry in AWX for that particular server:

root@AWX-panel:~# docker exec -i -t awx_task bash
bash-4.4# ssh-keygen -R matrix.fishbole.xyz
# Host matrix.fishbole.xyz found: line 25
/root/.ssh/known_hosts updated.
Original contents retained as /root/.ssh/known_hosts.old


11) Note the IP address generated during provision. Add new known_hosts record for the homeserver address:

root@AWX-panel:~# docker exec -i -t awx_task bash
bash-4.4# echo -e '# Custom DNS records for matrix.fishbole.xyz\n165.22.255.141 fishbole.xyz\n165.22.255.141 matrix.fishbole.xyz\n165.22.255.141 element.fishbole.xyz\n165.22.255.141 jitsi.fishbole.xyz' >> /etc/hosts


12) Remove the 'start' tag from the new '0 - Deploy/Update a Server'. As admin user, run that template with the following extra variable added:

`matrix_ssl_retrieval_method: none`


13A - (Admin Restore) Rsync /matrix, /chroot/website and the database into the server:

$ ssh matrix.fishbole.xyz
root@fishbole.xyz:~# sudo apt install rsync
root@fishbole.xyz:~# exit

$ rsync -av ./matrix/ matrix.fishbole.xyz:/matrix/
$ rsync -av ./chroot/website/ matrix.fishbole.xyz:/chroot/website/
$ rsync -av ./chroot/export/postgres_2021-06-12.sql.gz  matrix.fishbole.xyz:/chroot/export/

13B - (Admin Import) Copy export into /chroot/export/ with SCP, extract /matrix:

~/Documents$ scp ./chroot/export/* root@matrix.fishbole.xyz:/chroot/export/
matrix_2021-03-02.tar.gz                                            100% 6139KB 738.3KB/s   00:08
postgres_2021-03-02.sql.gz                                          100% 7496KB 796.3KB/s   00:09 

root@fishbole.xyz:~# tar -xvzf /chroot/export/matrix_2021-06-12.tar.gz -C /


14) Delete and re-create existing databases:

root@fishbole.xyz:~# docker exec -it matrix-postgres /bin/bash -c 'dropdb matrix'
root@fishbole.xyz:~# docker exec -it matrix-postgres /bin/bash -c 'dropdb matrix_ma1sd'
root@fishbole.xyz:~# docker exec -it matrix-postgres /bin/bash -c 'dropdb -f synapse'

bash-5.1$ createdb --template=template0 --encoding=UTF8 --locale=C matrix
bash-5.1$ createdb --template=template0 --encoding=UTF8 --locale=C matrix_ma1sd
bash-5.1$ createdb --template=template0 --encoding=UTF8 --locale=C synapse


15) Import the database dump:

Run the '00 - Restore and Import Postgresql Dump' job template with:
- member's Inventory
- member's deploy Project with setup.yml Playbook
- member's SSH Credential
- include all the extra variables found in /matrix/awx/extra_vars.json and the {{ server_path_postgres_dump }}, for example:

---
server_path_postgres_dump: /chroot/export/postgres_2021-06-12.sql.gz
plan_title: 'Micro DigitalOcean Server'
subscription_id: T-FKFAMCCR7CHX
member_id: 31
target: "matrix.fishbole.xyz"
matrix_domain: "fishbole.xyz"
matrix_awx_enabled: true


16) Remove the 'imposter-check' tag again and run 'Provision a New Server' again to load up the surveys from matrix_vars.yml


17) Copy the DNS information and send it to the customer so they can configure DNS again. For Example:

        "Your server has been created! You now need to configure your DNS to have the",
        "following records:",
        "Type    Host                    Priority  Weight  Port   Target",
        "A       -                       -         -       -      178.62.95.215",
        "A       -                       -         -       -      2a03:b0c0:1:d0::6df:e001",
        "A       matrix                  -         -       -      178.62.95.215",
        "A       matrix                  -         -       -      2a03:b0c0:1:d0::6df:e001",
        "CNAME   element                 -         -       -      matrix.fishbole.xyz",
        "CNAME   jitsi                   -         -       -      matrix.fishbole.xyz",
        "SRV     _matrix-identity._tcp   10        0       443    matrix.fishbole.xyz",
        "-",
        "Setting the IPv6 record is optional. If you need help doing this please contact us."


18) SSH into the old server and shut down the previous service:

`# systemctl stop matrix-synapse matrix-postgres matrix-ma1sd`


19) Wait for the DNS to propagate.


20) Run the new '0 - Deploy/Update a Server' job template again, then try and login.


21) If the new Matrix server works delete the old subscription with '00 - Ansible Delete Subscription', then re-provision the new subscription using 'Provision a New Server'.


22) If base domain isn't used (if matrix_nginx_proxy_base_domain_serving_enabled: true) then run the 'Configure Website + Access Export' job template again to enable the base domain site.
