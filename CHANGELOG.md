
# GoMatrixHosting v0.7.0

- CENTOS 8 EOL fix, curse you RedHat!! See[#33](https://gitlab.com/GoMatrixHosting/create-awx-system/-/issues/33)
- Add Mjolnir Bot section. See [#20](https://gitlab.com/GoMatrixHosting/ansible-provision-server/-/issues/20)
- Unclog discord-appservice-bot so it now works behind the wireguard proxy. See [#8](https://gitlab.com/GoMatrixHosting/matrix-docker-ansible-deploy/-/issues/8)
- Update deploy script readme and docs to reflect recent changes to GoMatrixHosting. See [#1654](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues/1654)


# Upgrade Notes v0.7.0

- Add the following section to every matrix_vars.yml file on AWX:
```
# Mjolnir Settings Start
matrix_bot_mjolnir_enabled: false
# Mjolnir Settings End
# Mjolnir Extension Start
matrix_bot_mjolnir_configuration_extension_yaml: |
  "homeserverUrl": "http://matrix-synapse:8008"
  "rawHomeserverUrl": "http://matrix-synapse:8008"
# Mjolnir Extension End
```
- Re-provision all servers.


# GoMatrixHosting v0.6.9

- Stop re-writing of matrix_homeserver_generic_secret_key variable. See[#13](https://gitlab.com/GoMatrixHosting/ansible-create-delete-subscription-membership/-/issues/13)


# GoMatrixHosting v0.6.8

- Upgraded create-awx-system to run on Debian 11. See [#26](https://gitlab.com/GoMatrixHosting/create-awx-system/-/issues/26).
- Removed the old ansible-tower-cli components from the AWX system, and upgraded the webhook and swatchdog roles to use the awx.awx ansible collection instead.
- Default to the hacks method to generate master token, the regular awx.awx modules are not reliable enough with AWX v0.17.1.
- We now auth directly against WordPress, removing the WPOAUTHServer plugin dependancy and greatly improving the panels login speed. See [#27](https://gitlab.com/GoMatrixHosting/create-awx-system/-/issues/27)[#22](https://gitlab.com/GoMatrixHosting/create-awx-system/-/issues/22).
- Added a [Contributing section to the create-awx-system README.md](https://gitlab.com/GoMatrixHosting/create-awx-system/-/blob/master/README.md#contributing).


# Upgrade Notes v0.6.8

- To the create-awx-system inventory file (vars.yml) add the following variable:
  `wp_username: username`
- Re-install AWX. (Take care to observe the new variables/changes to the setup-radius role.)
- Disable and remove the 'WP OAuth Server' plugin if you're using it, then cancel your subscription. :)

- Recommended: A full backup and recovery of your AWX system to Debian 11.


# GoMatrixHosting v0.6.7

- Major updates to the [recover-matrix-server](https://gitlab.com/GoMatrixHosting/gmhosting-external-tools/-/tree/main/recover-matrix-server) tool that automatically recover Matrix servers connected to AWx. See [#1](https://gitlab.com/GoMatrixHosting/gmhosting-external-tools/-/issues/1) tool. It's now faster and allows:
  - Recovering into a new member_id.
  - Recovering into a different subscription type.
  - Recovering to a new DigitalOcean region or on-premises location.
  - Preserving the previous subscriptions job templates history.
- Changed default usernames for accounts `@_janitor > @admin-janitor`, `@_dimension > @admin-dimension`, `@_mjolnir > @admin-mjolnir` due to `"Sending registration request...\nERROR! Received 400 Bad Request\nUser ID may not begin with _"` error.
- Added async timeout for media-repo size calculation.


# Upgrade Notes v0.6.7

- Edit matrix_vars.yml of every subscription so that:
```
awx_janitor_user_created: false
awx_dimension_user_created: false
awx_mjolnir_user_created: false
```
- Deploy/update all servers.


# GoMatrixHosting v0.6.6

- Create new [recover-matrix-server](https://gitlab.com/GoMatrixHosting/gmhosting-external-tools/-/tree/main/recover-matrix-server) tool for automated recovery of Matrix servers. See [#1](https://gitlab.com/GoMatrixHosting/gmhosting-external-tools/-/issues/1).
- Tested new [upgrade-distro tool](https://gitlab.com/GoMatrixHosting/gmhosting-external-tools/-/tree/main/upgrade-distro) for upgrading client servers to Debian 11. See [#7](https://gitlab.com/GoMatrixHosting/matrix-docker-ansible-deploy/-/issues/7).
- Add new '00 - Self-Check All Servers' template for bulk testing.
- Disable '00 - Backup All Servers' schedule if `backup_server_enabled: false`.
- New clearer naming scheme for DigitalOcean droplets `{{ subscription_id }}-{{ matrix_domain }}`.
- Changed default usernames for accounts `@janitor > @_janitor`, `@dimension > @_dimension`, `@mjolnir > @_mjolnir` so the client can use those usernames.
- Added 10m timeout for calculating size of media repositories.
- Fixed postgres version mismatch bug that was effecting backups.


# Upgrade Notes v0.6.6

- Update all your DigitalOcean droplets to the new naming scheme.
- Re-install AWX.


# GoMatrixHosting v0.6.5

- Upgraded the '00 - Deploy/Update All Servers Schedule' and '00 - Backup All Servers' so that they can now set more dynamic hourly, daily, weekly or monthly schedules. See [#23](https://gitlab.com/GoMatrixHosting/create-awx-system/-/issues/23).
- Add 'Force Upgrade' survey option to '00 - Deploy/Update All Servers' allowing the AWX admin to skip the repository check.
- Added the following new repository: [gmhosting-external-tools](https://gitlab.com/GoMatrixHosting/gmhosting-external-tools)
- Added forking notes to create-awx-system [README.md](https://gitlab.com/GoMatrixHosting/create-awx-system/-/blob/master/README.md)


# Upgrade Notes v0.6.5

- Add the following new vars.yml sections to create-awx-system:
```
# Update/Deploy All Settings
update_schedule_start: '20200101T000000'
update_schedule_frequency: 'HOURLY'
update_schedule_interval: 1
...
# Backup Server Settings
backup_schedule_start: 20200101T000000
backup schedule_frequency: 'DAILY'
backup_schedule_interval: 1
```
- Re-install AWX.


# GoMatrixHosting v0.6.4

- Fix FreeRADIUS/OAuth timeout issue. See [#21](https://gitlab.com/GoMatrixHosting/create-awx-system/-/issues/21).
- Upgraded Wireguard servers to support Debian 11.
- Update 'Rotate_AWX_Passwords_Keys.md' doc to include Wireguard server SSH rotation. See [#8](https://gitlab.com/GoMatrixHosting/ansible-create-delete-subscription-membership/-/issues/8).
- Added missing "ansible_connection: local" variable to AWX admins localhost.


# Upgrade Notes v0.6.4

- Re-install AWX.
- Re-provision all servers.


# GoMatrixHosting v0.6.3

- Automate generation of User Manuals from .odt file. See [#20](https://gitlab.com/GoMatrixHosting/create-awx-system/-/issues/20).
- Minor fixes to the still broken Corporal section.
- Add Discord AppService Bridge section. See [#9](https://gitlab.com/GoMatrixHosting/ansible-create-delete-subscription-membership/-/issues/9).


# Upgrade Notes v0.6.3

- Update every subscriptions matrix_vars.yml to include the new dividers:
```
$ ls /var/lib/awx/projects/clients/*/*/matrix_vars.yml
/var/lib/awx/projects/clients/user1/T-GD69EWZ4TRQ/matrix_vars.yml
/var/lib/awx/projects/clients/user2/T-DBLN3HX5SCV0/matrix_vars.yml
...
$ printf '# Bridge Discord AppService Start\n# Bridge Discord AppService End\n' >> /var/lib/awx/projects/clients/user1/T-GD69EWZ4TRQ/matrix_vars.yml
$ printf '# Bridge Discord AppService Start\n# Bridge Discord AppService End\n' >> /var/lib/awx/projects/clients/user2/T-DBLN3HX5SCV0/matrix_vars.yml
...
```
- Re-provision all servers.


# GoMatrixHosting v0.6.2

- Add new options to '0 - Configure Element' to alter the logo, logo link, headline and text. See [#22](https://gitlab.com/GoMatrixHosting/gomatrixhosting-matrix-docker-ansible-deploy/-/issues/22).
- Added alternative method for generating master token if it fails. See [this reddit thread](https://www.reddit.com/r/awx/comments/lastzb/awx_failed_to_get_token_the_read_operation_times/).
- Fix fragmented variable names, AWX related variables all begin with 'awx_' now.
- Batch up self-check tag tasks for easier reading.
- Remove whitespaces entered into matrix_domain before provision. See [#13](https://gitlab.com/GoMatrixHosting/ansible-provision-server/-/issues/13).


# Upgrade Notes v0.6.2

- Update variable names in every matrix_vars.yml:
```
# ls /var/lib/awx/projects/clients/*/*/matrix_vars.yml
```
Edit so that:
```
# AWX Settings Start
matrix_awx_enabled: true
matrix_awx_janitor_user_password: 6304d28ed0f56397c4de241a634ab845
matrix_awx_janitor_user_created: true
matrix_awx_dimension_user_password: e3373a103ecbf9c66d8a802540e2a4f8
matrix_awx_dimension_user_created: true
matrix_awx_mjolnir_user_password: 87b86cf34d4ad1ce5cd0910fd0de3e77
matrix_awx_mjolnir_user_created: true
matrix_awx_backup_enabled: falses
# AWX Settings End
...
# Corporal Settings Start
matrix_corporal_enabled: false
matrix_corporal_policy_provider_mode: 'Simple Static File'
matrix_corporal_simple_static_config: ''
matrix_corporal_pull_mode_uri: 'https://intranet.example.com/matrix/policy'
matrix_corporal_raise_ratelimits: 'Raised'
matrix_corporal_pull_mode_token: ''
matrix_corporal_http_api_auth_token: ''
# Corporal Settings End
...
# Custom Settings Start
ext_recaptcha_private_key: "private-key"
ext_recaptcha_public_key: "public-key"
ext_enable_registration_captcha: true
sftp_auth_method: 'Disabled'
sftp_password: ''
sftp_public_key: ''
customise_base_domain_website: false
# https://github.com/ma1uta/ma1sd/blob/master/docs/stores/README.md
ext_matrix_ma1sd_auth_store: 'Synapse Internal'
ext_matrix_ma1sd_configuration_extension_yaml: ["matrix_ma1sd_configuration_extension_yaml: |", "  ldap:", "    enabled: true", "    connection:", "      host: ldapHostnameOrIp", "      tls: false", "      port: 389", "      baseDNs: [\'OU=Users,DC=example,DC=org\']", "      bindDn: CN=My ma1sd User,OU=Users,DC=example,DC=org", "      bindPassword: TheUserPassword"]
ext_dimension_users_raw: []
ext_federation_whitelist_raw: []
ext_url_preview_accept_language_default: ["en"]
# Custom Settings End
```
becomes:
```
# AWX Settings Start
matrix_awx_enabled: true
awx_janitor_user_password: 6304d28ed0f56397c4de241a634ab845
awx_janitor_user_created: true
awx_dimension_user_password: e3373a103ecbf9c66d8a802540e2a4f8
awx_dimension_user_created: true
awx_mjolnir_user_password: 87b86cf34d4ad1ce5cd0910fd0de3e77
awx_mjolnir_user_created: true
awx_backup_enabled: falses
# AWX Settings End
...
# ma1sd Settings Start
...
# https://github.com/ma1uta/ma1sd/blob/master/docs/stores/README.md
awx_matrix_ma1sd_auth_store: 'Synapse Internal'
awx_matrix_ma1sd_configuration_extension_yaml: ["matrix_ma1sd_configuration_extension_yaml: |", "  ldap:", "    enabled: true", "    connection:", "      host: ldapHostnameOrIp", "      tls: false", "      port: 389", "      baseDNs: [\'OU=Users,DC=example,DC=org\']", "      bindDn: CN=My ma1sd User,OU=Users,DC=example,DC=org", "      bindPassword: TheUserPassword"]
# ma1sd Settings End
...
# Synapse Settings Start
...
awx_enable_registration_captcha: false
awx_recaptcha_public_key: public-key
awx_recaptcha_private_key: private-key
awx_federation_whitelist: []
awx_url_preview_accept_language_default: ["en"]
# Synapse Settings End
...
# Corporal Settings Start
matrix_corporal_enabled: false
awx_corporal_policy_provider_mode: 'Simple Static File'
awx_corporal_simple_static_config: ''
awx_corporal_pull_mode_uri: 'https://intranet.example.com/matrix/policy'
awx_corporal_raise_ratelimits: 'Raised'
awx_corporal_pull_mode_token: ''
awx_corporal_http_api_auth_token: ''
# Corporal Settings End
...
# Dimension Settings Start
...
awx_dimension_users: []
# Dimension Settings End
...
# Custom Settings Start
awx_customise_base_domain_website: false
awx_sftp_auth_method: 'Disabled'
awx_sftp_password: ''
awx_sftp_public_key: ''
# Custom Settings End
```
- Also edit variable names in:
```
# ls /var/lib/awx/projects/clients/*/*/borg_backup.yml
```
Replacing:
```
matrix_awx_backup_encryption_passphrase: dec7543661db8e84258aebce0cbecec4
```
With:
```
awx_backup_encryption_passphrase: dec7543661db8e84258aebce0cbecec4
```
- Also edit every provision jobs survey renaming `element_subdomain` to `awx_element_subdomain`.
- Re-provision all servers.

# GoMatrixHosting v0.6.1

- Use proper 'awx.awx.tower_token' module method to generate a persistent 'master token' then 'session tokens' for each individial run. Avoids storing the AWX admins password in plaintext on the AWX server. See [#2](https://gitlab.com/GoMatrixHosting/matrix-docker-ansible-deploy/-/issues/2) and [#13](https://gitlab.com/GoMatrixHosting/gomatrixhosting-matrix-docker-ansible-deploy/-/issues/13).
- Disable scm_update_on_launch on new users deploy project and make the hourly "Deploy/Update All Servers" update those projects, improves the speed of deploy stage jobs. See [#7](https://gitlab.com/GoMatrixHosting/ansible-create-delete-subscription-membership/-/issues/7).


# Upgrade Notes v0.6.1

- Reinstall AWX.
- For every "matrix_domain - Matrix Docker Ansible Deploy' project in AWX, manually edit it, then uncheck the "Update Revision on Launch" checkbox:
`https://panel.example/#/projects`


# GoMatrixHosting v0.6.0

- Fix previously added subscription deletion playbooks.
- Update README.md files for each repository.
- Document AWX password and SSH keys rotation, see [#17](https://gitlab.com/GoMatrixHosting/create-awx-system/-/issues/17).


# Upgrade Notes v0.6.0

- Delete previous borg backup keys for AWX:
`$ rm ~/.ssh/borg_{{ awx_url }}_ed25519`
- Delete previous client > backup keys:
`$ rm /var/lib/awx/projects/hosting/backup_*.key`
- Remove old backup keys entry for clients from the backup server:
`$ sed '/^command="borg serve --restrict-to-path {{ backup_server_directory }}/Clients",restrict ssh-ed25519/d' /home/{{ backup_server_user }}/.ssh/authorized_keys`
- Remove the following variables from the create-awx-system vars.yml:
```
backup_private_ssh_key: /home/user/.ssh/backups3_ed25519
backup_public_ssh_key: /home/user/.ssh/backups3_ed25519.pub
```
- Reinstall AWX.
- Re-provision all servers.


# GoMatrixHosting v0.5.9

- Use underscores instead of dashes for playbooks/task lists.
- Alter end-subscription logic, schedules deletion after 0 (immediate) to N hours and stops the matrix services. Data export is still possible before deletion. The deletion can be cancelled by the administrator, removing the schedule and starting the Matrix services again. See [#5](https://gitlab.com/GoMatrixHosting/ansible-create-delete-subscription-membership/-/issues/5).


# Upgrade notes for v0.5.9

- Rename `prometheus_retention_period` variable in create-awx-system vars.yml to `prometheus_days_retention`.
- Add new `delete_subscription_hours_delay: 48` value to create-awx-system vars.yml.
- Do a complete re-install of AWX.
- Delete the following administrator job templates:
```
00 - Ansible Create Account
00 - Ansible Create Manual Subscription
00 - Ansible Create MP Subscription
00 - Ansible Delete Membership
00 - Ansible Delete Subscription
```


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
