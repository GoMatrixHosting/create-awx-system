
# GoMatrixHosting v0.5.9

- Use underscores instead of dashes for task lists.
- Alter end-subscription logic, schedule deletion after N hours.

# Upgrade notes for v0.5.9

- Rename `prometheus_retention_period` variable in create-awx-system vars.yml to `prometheus_days_retention`.
- Add new `delete_subscription_hours_delay: 48` value to create-awx-system vars.yml.
- Run configure-awx role again on the AWX tower:
`$ ansible-playbook -v -i ./inventory/hosts -t "configure-awx" post_setup.yml`


# GoMatrixHosting v0.5.8

- Add automated 'Deploy/Update All Servers' job to apply updates within the hour. See [#18](https://gitlab.com/GoMatrixHosting/gomatrixhosting-matrix-docker-ansible-deploy/-/issues/18).


# Upgrade notes for v0.5.8

- In AWX delete the 'Ansible Create Delete Subscription Membership' project.
- In AWX delete the 'Unlock SSH Password' credential.
- Run configure-awx role again on the AWX tower:
`$ ansible-playbook -v -i ./inventory/hosts -t "configure-awx" post-setup.yml`
- In AWX delete the "{{ org_name }} Inventory" inventory.
- In AWX delete the "{{ org_name }}" organisation.
- In AWX delete the deploy/update schedule of all existing subscriptions.


# GoMatrixHosting v0.5.7

- Prevent Provision stage re-writing variables it should only write on the first run, see [#12](https://gitlab.com/GoMatrixHosting/ansible-provision-server/-/issues/12).
- Fix SFTP website upload, see [#10](https://gitlab.com/GoMatrixHosting/gomatrixhosting-matrix-docker-ansible-deploy/-/issues/10).


# GoMatrixHosting v0.5.6

- Document and test upgrades/downgrades of subscriptions. See [#10](https://gitlab.com/GoMatrixHosting/ansible-provision-server/-/issues/10).


# Upgrade notes for v0.5.6

- Add 'plan_title' to the extra_vars.json file of all existing subscriptions.
`  "plan_title": "Small DigitalOcean Server",`
- Add 'plan_title' to the extra variables GUI for every provision job_template.
- Remove plan_title from the server_vars.yml file of all existing subscriptions.
`sed -i '/plan_title/d' /var/lib/awx/projects/clients/*/*/server_vars.yml`
- Re-provision all servers.


# GoMatrixHosting v0.5.5

- Set prometheus retention period as variable in create-awx-system.
- Fixed minor bugs relating to ma1sd/LDAP.
- Update the borg backup config to include the rest of /matrix and custom website folder, also fixed issue where re-provisioning blanks the recaptcha section of the 'Configure Synapse' survey, solves 'Create AWX System' issue [#16](https://gitlab.com/GoMatrixHosting/create-awx-system/-/issues/16).
- Set locale of all client servers to en_US to avoid 'Ansible Provision Server' issue [#11](https://gitlab.com/GoMatrixHosting/ansible-provision-server/-/issues/11).
 

# Upgrade notes for v0.5.5

- Add new prometheus_retention_period variable to create-awx-system inventory:
`prometheus_retention_period: 28`
- Reconfigure the monitor section of AWX:
`$ ansible-playbook -v -i ./inventory/hosts -t "setup,setup-monitor,setup-webhooks" pre-setup.yml`
- Re-provision all servers.


# GoMatrixHosting v0.5.4

- Install and configure unattended-upgrades on all servers.
- Fix bug with 'Purge Media' template and wireguarded servers.
- Fix bug where 'Configure Website + Access Export' breaks the SSH config.
- Update backup/restore and export process to include client website /chroot/website.
- Fixed bug where 'purge media' uses seconds timestamp and not milliseconds.


# Upgrade notes for v0.5.4

- Re-provision all servers.
- Run pre-setup.yml again on AWX:
`$ ansible-playbook -v -i ./inventory/hosts -t "setup" pre-setup.yml`


# GoMatrixHosting v0.5.3

- Add DNS advice to Wireguard provision.
- Add node-exporter with custom port to Wireguard servers.
- Add node-exporter to backup server.
- Update generate_config.sh which generates Prometheus configuration.
- Update Recover_AWX_Server.md notes.


# Upgrade notes for v0.5.3

- Add new hosting_url variable to your 'create-awx-system' vars.yml file, set it as the domain of your front-end site:
`hosting_url: gomatrixhosting.com`
- Re-install AWX, observe the new instructions in /doc/Installation_AWX.md.
- Remove /root/bin folder from AWX system.
- Manually add 'backup.{{ hosting_url }}' host to all existing client inventories, with the following variables:
```
ansible_host: '{{ backup_server_ip }}'
ansible_port: '{{ backup_server_ssh_port }}'
```
- Manually remove 'Backup Server' host from all existing client inventories.
- Re-provision all existing Wireguard servers.


# GoMatrixHosting v0.5.2

- Replaced poorly designed method for assigning hosts to groups in AWX with a URI module call.
- Make '00 - Ansible Delete Membership' more reliable, ensure client-list entry is deleted
- Update notes on setting up Google ReCaptcha for registration.
- Fix matrix-awx bug where the registrations_require_3pid variable aren't removed if disabled.


# GoMatrixHosting v0.5.1

- Add '00 - Create Wireguard Server' template for AWX admin to provision Wireguard servers that on-premises servers can use to connect.
- Subscription involved can view an additional '0 - {{ subscription_id }} - Provision Wireguard Server' template.
- Add /docs/Setup_Wireguard_Server.md guide.
- Add onboarding script for Windows 10 users.
- Raise maximum download size to 200MB.

# Upgrade notes for v0.5.1

- Re-configure awx with 'create-awx-system' script:
```
$ ansible-playbook -v -i ./inventory/hosts -t "configure-awx" post-setup.yml
```


# GoMatrixHosting v0.5.0

- Avoid keeping a copy of the media repository locally, saves space in /chroot/export.
- Improve synchronization with backups and exports between the copying the configs + media repository and the database snapshot.
- Improve recovery process to ensure downtime only during DNS changes.
- Add 'Export Server' job template for generating SFTP export.
- Fix for broken SSL renewal on AWX.
- Fixed a bug with deleting subscriptions.

# Upgrade notes for v0.5.0

- Move/Delete previous borg backup files from backup server.
```
root@backup-server:~# cp -R /backup_directory/Clients /backup_directory/Clients-old
root@backup-server:~# rm -r /backup_directory/Clients/* 
```
- Re-provision all servers.


# GoMatrixHosting v0.4.9

- added new 'Configure Email Relay' section, which allows the user to easily enable a Mailgun relay for sending verification emails.

# Upgrade notes for v0.4.9

- Reinstall AWX with new inventory settings.
- Add Email section with a new password to each subscribers matrix_vars.yml:
```
# Email Settings Start
matrix_mailer_sender_address: "verify@mail.example.org"
matrix_mailer_relay_use: false
matrix_mailer_relay_host_name: "smtp.mailgun.org"
matrix_mailer_relay_host_port: 587
matrix_mailer_relay_auth: true
matrix_mailer_relay_auth_username: "user@mail.example.org"
matrix_mailer_relay_auth_password: << strong-password >>
# Email Settings End
```
- Add 'setup-mailgun' tag to every subscribers provision template.
- Re-provision all servers.


# GoMatrixHosting v0.4.8

- fix AWX issue causing synapse registration secret to remain blank in homeserver.yaml.
- added seperate job template for adjusting Element client subdomain.
- adjusted firewall rules for matrix-mailer.
- fix fault in 'backup-all' job template.

# Upgrade notes for v0.4.8

- Re-provision all servers.


# GoMatrixHosting v0.4.7

- reinvented database purging section, separated final shrinking that causes downtime.
- fixed AWX issue causing rust-synapse-compress-state section to not execute.
- added more reliable script method of generating the total room list.

# Upgrade notes for v0.4.7

- Re-provision all servers.


# GoMatrixHosting v0.4.6

- Add database purge section.
- Add markdown copy of User manual.
- Tweak compress state find rooms timeout.
- Update compile AWX instructions for custom branding and radius fix.

# Upgrade notes for v0.4.6

- Re-provision all servers.
- Add these variables to each matrix_vars.yml:
```
matrix_awx_mjolnir_user_password: << strong-password >> 
matrix_awx_mjolnir_user_created: false
```


# GoMatrixHosting v0.4.5

Fix remote and local media purge
base_domain_used can now be seamlessly changed after initial provision
Jitsi now disabled for Micro to Medium sized droplets
Minor fixes


# GoMatrixHosting v0.4.4

Create new 'Access Export' playbook for subscriptions that aren't hosting the base domain through AWX.
Allow metrics ports in firewall.
Update postgresql tuning and change default cache factor.
Added swappiness settings.
User manual updates.
Added a changelog with upgrade notes for AWX.

# Upgrade notes for v0.4.4

- Delete '{{ matrix_domain }} - 1 - Configure Website + Access Export from every 'base_domain_used=true' server, re-provision.
- Delete 'customise_base_domain_website' variable in every 'base_domain_used=true' servers matrix_vars.yml in AWX
- Set 'matrix_synapse_caches_global_factor' to '4.0' in every servers matrix_vars.yml in AWX


# GoMatrixHosting v0.4.3

Minor fixes.
Variable name change for matrix_synapse_use_presence.


# GoMatrixHosting v0.4.2

Various fixes.
Added purge local/remote media function.


# GoMatrixHosting v0.4.1

Minor fixes for deploying new AWX setup
Added and tested minimal AWX setup instructions


# GoMatrixHosting v0.4.0

Fixed the client machine backups and 'Backup-all' functions.
Added 'Provision-All' job template.
Added Dimension integration server section.
Auto-create @dimension user.
Cache matrix_vars.yml to avoid corrupting the original.


# GoMatrixHosting v0.3.2

Minor fix to install jq on AWX if monitor not installed.
Fix to allow include_tasks to work properly.
Fix to limit max filesize limit to 100MB.


# GoMatrixHosting v0.3.1

hotfix to allow running outside AWX


# GoMatrixHosting v0.3.0

Added worker support for larger instances.
Added room complexity limits for smaller servers.
Added postgresql tuning based on size of plan.
Update system to AWX 17.1.0.
Refined/fixed radius authentication.
Added opt-in backups for client servers, and admin script to run them all sequentially.
Added firewalling to client servers.
Removed MAU limitations.
Revised documentation.


# GoMatrixHosting v0.2.1

Added documentation for deploy script.
Revises matrix-nginx-proxy template to avoid intruding on that role.
Revised SFTP access to export and website files, allow setting SSH publickey access instead of password.
Added 'production/testing' modes to AWX.
Other minor fixes.


# GoMatrixHosting v0.2.0

Use Oauth token to alter AWX system.
Added Manual Subscription creation mode.
Added ma1sd LDAP/AD and Matrix Corporal sections.
Secure SSH credentials with vault.


# GoMatrixHosting v0.1.0 - The initial release.

Initial version of the GoMatrixHosting system, allows for seamless login integration with a commercial WordPress site. On-premise plans enabled.
Radius system connects AWX to WordPress, Swatchdog monitors logins to assign a 'enterprise user' to the necessary team when they first login.
