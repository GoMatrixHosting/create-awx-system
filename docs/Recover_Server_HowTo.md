

1) Extract variables needed to re-create subscription:

On controller, extract matrix.tar.gz, examine /matrix/awx/organisation.yml and /matrix/awx/server_vars.yml and extra_vars.yml, copy:

- subscription_id: I-CREUS74S6969			[/matrix/awx/extra_vars.yml]
- member_id: 31						[/matrix/awx/extra_vars.yml]
- client_email: "bobfett@protonmail.com"		[/matrix/awx/organisation.yml]
- client_first_name: "Bob"				[/matrix/awx/organisation.yml]
- client_last_name: "Fett"				[/matrix/awx/organisation.yml]
- plan_title: Small Server				[/matrix/awx/server_vars.yml]
- byo_bool: False					[/matrix/awx/server_vars.yml]


2) Observe 'plan_title' and 'byo_bool' in server_vars.yml, if it's a MP subscription launch '00 - Ansible Create MP Subscription' with the above variables, otherwise launch '00 - Ansible Create BYO Subscription'.


3) Before provisioning look at matrix_vars.yml, with that and the previous files record:

- matrix_domain: fishbole.xyz				[/matrix/awx/matrix_vars.yml]
- do_droplet_region: tor1				[/matrix/awx/server_vars.yml]
- matrix_server_fqn_element: element.fishbole.xyz	[/matrix/awx/matrix_vars.yml]
- matrix_nginx_proxy_base_domain_serving_enabled: true	[/matrix/awx/matrix_vars.yml]


4) Provision with these survery answers:

SET BASE DOMAIN - matrix-domain

BASE DOMAIN USED - If matrix_nginx_proxy_base_domain_serving_enabled: true, then select 'false', otherwise select 'true'. 

SET ELEMENT SUBDOMAIN - Copy only the subdomain from matrix_server_fqn_element, for example only 'element' out of element.gnuperth.org.

SELECT REGION - Figure it out from the do_droplet_region. (Or a different one if you're trying to migrate it)


5) Copy the DNS information and send it to the customer so they can configure DNS again. For Example:

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


6) Comment out the backup.sh in roots crontab.


7) Load matrix_vars.yml from backup into AWX:

root@AWX-panel:~# nano /var/lib/awx/projects/clients/31/I-CREUS74S6969/matrix_vars.yml

HERE

8) As admin user, after the DNS is updated, run 'Deploy/Update a Server' without the 'start' tag. This is needed to initialise docker for the 'setup-nginx' tag we use in the next step.


9A - Admin Upload) Copy backup into /chroot/backup/ with SCP:

~/Documents/export$ scp ./* root@matrix.fishbole.xyz:/chroot/backup/
matrix.tar.gz                                                          100% 8288KB 703.3KB/s   00:11
postgres_2020-12-20.sql.gz                                             100%   35KB  89.8KB/s   00:00


9B - User Upload) As admin user, run 'Configure Website + Access Backup' without the 'start' tag.

Then SFTP in and import the backup data you previously exported.

sftp> put -r /home/chatoasis/Documents/export/* ./backup/
Uploading /home/chatoasis/Documents/export/matrix.tar.gz to /./backup/matrix.tar.gz
/home/chatoasis/Documents/export/matrix.tar.gz                         100% 8288KB 779.4KB/s   00:10
Uploading /home/chatoasis/Documents/export/postgres_2020-12-20.sql.gz to /./backup/postgres_2020-12-20.sql.gz
/home/chatoasis/Documents/export/postgres_2020-12-20.sql.gz            100%   35KB 153.0KB/s   00:00


10) Import the database dump:

Run the '00 - Restore and Import Postgresql Dump' job template, 
with 'import-postgres' and 'import-awx' tags, 
with specific clients project, inventory and ssh credential,
include all the extra variables found in /matrix/awx/extra_vars.yml and the {{ server_path_postgres_dump }}, for example:

---
server_path_postgres_dump: /chroot/backup/postgres_2020-12-20.sql.gz
subscription_id: I-CREUS74S6969
member_id: 31
target: "matrix.fishbole.xyz"
matrix_domain: "fishbole.xyz"
matrix_awx_enabled: true


11) Run 'Provision a New Server' again to load up the surveys from matrix_vars.yml


12) Run 'Start/Restart all Services' job template, then try and login.




.


