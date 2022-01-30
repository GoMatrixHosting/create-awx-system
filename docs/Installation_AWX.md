# GoMatrixHosting AWX Setup - Installation Instructions


# Create a server

Create a Debian 11 server with at least 8GB or RAM and setup SSH access to root user.
```
$ ssh root@panel.example.org
$ exit
```

# Setup DNS entry for it:

Map an A/AAAA record for panel.example.org to the servers IP.

Optionally:
Map a CNAME record for rancher.example.org to panel.example.org.
Map a CNAME record for monitor.example.org to panel.example.org.


# Installation

1) Optionally, create a backup server. You should be able to access root using a IP that the AWX server can reach and the 'client_private_ssh_key', it should also contain a depriviledged user 'backup_server_user' and backup location 'backup_server_location'. Collect its SSH fingerprint and save it to 'backup_server_ssh_fingerprint', to collect it run this command:

$ ssh-keyscan -t ed25519 {{ backup_server_ip }} 2>/dev/null
255.150.40.99 ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOdNgn7zqlpWIsiTV91QLEtRnXH18uMC27zVJYHsql/D

Create a A/AAAA record for backup.example.org pointing to the backup servers IP.

Install prometheus-node-exporter and export port 9100 on the backup server.


2A) Pre-setup, setup before the awx playbook is run, installs Docker and sets up TLS proxy for AWX, optionally website hooks and grafana are also setup.

`$ git clone https://gitlab.com/GoMatrixHosting/create-awx-system.git`


B) Generate a SSH key for dialing into client servers, ensure it has a strong password:
```
$ ssh-keygen -t ed25519 -f '/home/username/.ssh/example_clients' -C "Example AWX to Client Key"
Generating public/private ed25519 key pair.
Enter passphrase (empty for no passphrase): 
Enter same passphrase again:
```


C) Create an isolated user account on GitLab with no access to your other repositories/groups. Then with that user account create a private repository for the AWX systems /projects folder:

https://gitlab.com/isolateduser/vars_panel.example.org.git

Replace the 'https://' with '@' to create the GitLab API link:

@gitlab.com/isolateduser/vars_panel.example.org.git

Finally create a read/write access token for that user and record it into vars.yml: https://gitlab.com/-/profile/personal_access_tokens


D) Edit host into: ./inventory/hosts

Create folder for host at: ./inventory/host_vars/panel.example.org/

Record these variables to ./inventory/host_vars/panel.example.org/vars.yml:

- org_name 			(The name of your organisation.)
- hosting_url			(The URL of your organisation.)
- awx_url 			(The URL for AWX.)
- grafana_url 			(The URL for Grafana.)
- certbot_email 		(The organisations email.)
- grafana_admin_password	(Graphana admin users password.)
- prometheus_retention_period	(Number of days to retain the monitoring data.)
- secret_key			(Strong password for the AWX secrets.)
- pg_password			(Strong password for the AWX database.)
- admin_password 		(Strong password for the AWX admin user.)
- delete_subscription_hours_delay	(The number of hours to delay the subscription deletion.)
- update_schedule_start		(The start time for scheduled client updates in 'YYYYMMDDTHHMMSS' format, for example '20211030T080000' which means the 30th of October 2021 at 8AM.)
- update_schedule_frequency	(The time period for scheduled client updates, options are 'MINUTELY', 'HOURLY', 'DAILY', 'WEEKLY','MONTHLY')
- update_schedule_interval	(The number of minutes/hours/days/weeks/months to schedule client updates to.)
- create_delete_source		(Repository URL for 'Ansible Create Delete Subscription Membership'.)
- create_delete_branch		(Branch of this repository to use.)
- provision_source		(Repository URL for 'Ansible Provision'.)
- provision_branch		(Branch of this repository to use.)
- deploy_source			(Repository URL for 'matrix-docker-ansible-deploy'.)
- deploy_branch			(Branch of this repository to use.)
- client_public_ssh_key 	(Location of public client key AWX will use.)
- client_private_ssh_key 	(Location of private client key AWX will use.)
- client_private_ssh_key_password 	(Strong password for this private key.)
- vault_unlock_ssh_password:	(Strong password to vault the private_ssh_key_password.)

If you will be using the Mailgun relay (recommended), define:
- mg_sender_email_address	(The Mailgun email address. eg: "user@mail.example.org")
- mg_sender_domain		(The Mailgun email domain. eg: "mail.example.org"
- mg_relay_host_name		(The Mailgun relay host name. eg: "smtp.mailgun.org")
- mg_api_url			(The Mailgun API location. eg: "api.mailgun.net")
- mg_private_api_key		(The Mailgun private API key.)

If you will be using a backup server (recommended), define:
- backup_server_enabled		('true' if using a backup server, otherwise 'false')
- backup_server_ip 		(IP address of the backup server.)
- backup_server_hostname 	(The hostname of the backup server.)
- backup_server_user 		(The username of the backup server.)
- backup_server_directory 	(The directory to backup to on the backup server.)
- backup_server_location:	(The location of the backup server.)
- backup_awx_encryption_passphrase 	(Strong password for the AWX borg backup.)
- backup_server_ssh_fingerprint (The host SSH fingerprint of your backup server.)
- backup_schedule_start		(The start time for scheduled client backups in 'YYYYMMDDTHHMMSS' format, for example '20211030T080000' which means the 30th of October 2021 at 8AM.)
- backup_schedule_frequency	(The time period for schedules client backups, options are 'MINUTELY', 'HOURLY', 'DAILY', 'WEEKLY','MONTHLY')
- backup_schedule_interval	(The number of minutes/hours/days/weeks/months to schedule client backups to.)

If you want to spawn Matrix servers using DigitalOcean, define:
- do_api_token 			(Your DigitalOcean API token/)
- do_spaces_access_key 		(Your DigitalOcean Spaces Access Key.)
- do_spaces_secret_key 		(Your DigitalOcean Spaces Secret Key.)
- do_image_master 		(eg: debian-10-x64)

If you will be using this setup commercially (with WordPress/MemberPress), define:
- radius_secret			(Strong password for authenticating AWX against FreeRadius.)
- oauth_client_id		(client_id from WP Oauth Server WordPress plugin.)
- oauth_client_secret		(client_secret from WP Oauth Server WordPress plugin.)
- wp_url			(The URL of the front-end WordPress site.)
- wp_username			(The front-end WordPress username you SSH into.)

Run the script:

`$ ansible-playbook -v -i ./inventory/hosts -t "setup,setup-rancher,setup-monitor,generate-token,configure-awx,setup-webhooks,setup-radius,setup-swatchdog,setup-backup,enable-backup" post_setup.yml`


3) If using a backup server, perform the initial SSH handshake from AWX to backup server.

From AWX:
`# ssh {{ backup_server_hostname }}`

Note the command-line here is restricted, so you won't be able to do anything besides connnect.


4A) If using this setup commercially (with WordPress/MemberPress), perform the initial SSH handshake from AWX to the wordpress site:

From AWX:
`# runuser -u freerad -- /usr/bin/ssh {{ wp_url }} ./wp-probe.sh admin test`

This should print the following error:
```
Error: Invalid user ID, email or login: 'admin'
1
```

4B) check webhook.service status:
```
# systemctl status webhook.service 
● webhook.service
     Loaded: loaded (/etc/systemd/system/webhook.service; enabled; vendor preset: enabled)
     Active: active (running) since Thu 2022-01-06 00:35:33 UTC; 10min ag
```


5) Connect AWX to FreeRADIUS server

In the 'Authentication' > 'Radius' page:

RADIUS SERVER:	Public IP of the AWX server.
RADIUS PORT:	1812
RADIUS SECRET:	"{{ radius_secret }}"


6) Set base URL in AWX

Settings > Miscellaneous System Settings > Edit

Change 'Base URL of the Tower host' to your AWX systems URL.


7) Setup grafana.

The Grafana needs extra configuration to work, follow the [Grafana.md in the docs/ directory](docs/Grafana.md).

