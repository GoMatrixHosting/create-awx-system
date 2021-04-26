
# GoMatrixHosting v0.4.4


# Upgrade notes for v0.4.4

- Delete '{{ matrix_domain }} - 1 - Configure Website + Access Export from on-premises servers, re-provision.
- Delete 'customise_base_domain_website' variable in every on-premises subscribers matrix_vars.yml in AWX
- Set 'matrix_synapse_caches_global_factor' to '4.0' in every subscribers matrix_vars.yml in AWX


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


# GoMatrixHosting v0.1.0

Initial version of the GoMatrixHosting system, allows for seamless login integration with a commercial WordPress site. On-premise plans enabled.
Radius system connects AWX to WordPress, Swatchdog monitors logins to assign a 'enterprise user' to the necessary team when they first login.
