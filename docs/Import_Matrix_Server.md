
~~ Import Matrix Server ~~

1) Extract variables needed to re-create subscription:

On controller, extract matrix.tar.gz, examine /matrix/awx/organisation.yml and /matrix/awx/matrix_awx.yml and /matrix/awx/server_vars.yml and /matrix/awx/extra_vars.json, copy:

- client_email: "bobfett@protonmail.com"		[/matrix/awx/organisation.yml]
- client_first_name: "Bob"				[/matrix/awx/organisation.yml]
- client_last_name: "Fett"				[/matrix/awx/organisation.yml]
- matrix_server_fqn_element: element.fishbole.xyz	[/matrix/awx/matrix_vars.yml]
- matrix_nginx_proxy_base_domain_serving_enabled: true	[/matrix/awx/matrix_vars.yml]
- plan_title: Small DigitalOcean Server			[/matrix/awx/server_vars.yml]
- subscription_type: digitalocean			[/matrix/awx/server_vars.yml]
- matrix_domain: fishbole.xyz				[/matrix/awx/extra_vars.yml]
- subscription_id: I-CREUS74S6969			[/matrix/awx/extra_vars.yml]
- member_id: 31						[/matrix/awx/extra_vars.yml]

As well as:

- do_droplet_region: tor1				[/matrix/awx/server_vars.yml]
OR
- server_ipv4: 134.209.44.206				[/matrix/awx/server_vars.yml]
- server_ipv6: 2604:a880:800:c1::181:7001		[/matrix/awx/server_vars.yml]


2) Observe 'subscription_id' in server_vars.yml, if it's a MemberPress subscription (Starts with I-) launch '00 - Ansible Create MP Subscription' with the above variables, otherwise if it's a manual subscription (Starts with T-) launch '00 - Ansible Create Manual Subscription'.


3) Provision with these survey answers:

SET BASE DOMAIN - matrix_domain

BASE DOMAIN USED - If matrix_nginx_proxy_base_domain_serving_enabled: true, then select 'false', otherwise select 'true'. 

SET ELEMENT SUBDOMAIN - Copy only the subdomain from matrix_server_fqn_element, for example only 'element' out of element.gnuperth.org.

SELECT REGION - Figure it out from the do_droplet_region. (Or a different one if you're trying to migrate it)


4) Edit Deploy/Update a Server to not include the 'start' tag.


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


6) Login to the new server and comment out the export.sh in root users crontab.


7) Load matrix_vars.yml from the restored backup into AWX:

~/Documents$ tar -xf ./chroot/export/matrix.tar.gz
~/Documents$ scp ./awx/matrix_vars.yml panel.topgunmatrix.com:/var/lib/awx/projects/clients/billy.bob/T-FKFAMCCR7CHX/
matrix_vars.yml                               100% 3840    13.1KB/s   00:00 


8) Clear known_hosts entry in AWX for that particular server:

root@AWX-5-panel:~# docker exec -i -t awx_task bash
bash-4.4# sed '/^matrix.fishbole.xyz/d' -i /root/.ssh/known_hosts


9) As admin user, after the DNS is updated, run 'Deploy/Update a Server' without the 'start' tag. This is needed to initialise docker for the 'setup-nginx' tag we use in the next step.


10A - (Admin Upload) Copy backup into /chroot/export/ with SCP:

~/Documents$ scp ./chroot/export/* root@matrix.fishbole.xyz:/chroot/export/
matrix.tar.gz                                                       100% 6139KB 738.3KB/s   00:08
postgres_2021-03-02.sql.gz                                          100% 7496KB 796.3KB/s   00:09 



10B - (User Upload) As admin user, run 'Configure Website + Access Export' without the 'start' tag.

Then SFTP in and import the backup data you previously exported.

sftp> put -r /home/chatoasis/Documents/chroot/export/* ./export/
Uploading /home/chatoasis/Documents/export/matrix.tar.gz to /./export/matrix.tar.gz
/home/chatoasis/Documents/export/matrix.tar.gz                        100% 8288KB 779.4KB/s   00:10
Uploading /home/chatoasis/Documents/chroot/export/postgres_2021-03-02.sql.gz to /./export/postgres_2021-03-02.sql.gz
/home/chatoasis/Documents/chroot/export/postgres_2021-03-02.sql.gz    100%   35KB 153.0KB/s   00:00


11) Import the database dump:

Run the '00 - Restore and Import Postgresql Dump' job template, 
with 'import-postgres' and 'import-awx' tags, 
with specific members deploy project, inventory and ssh credential,
include all the extra variables found in /matrix/awx/extra_vars.yml and the {{ server_path_postgres_dump }}, for example:

---
server_path_postgres_dump: /chroot/export/postgres_2020-12-20.sql.gz
subscription_id: I-CREUS74S6969
member_id: 31
target: "matrix.fishbole.xyz"
matrix_domain: "fishbole.xyz"
matrix_awx_enabled: true


12) Run 'Provision a New Server' again to load up the surveys from matrix_vars.yml


12) Uncomment export.sh from toot users crontab.


13) Run 'Start/Restart all Services' job template, then try and login.


