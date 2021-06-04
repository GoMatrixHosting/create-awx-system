
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
