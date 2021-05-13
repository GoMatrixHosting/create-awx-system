
GoMatrixHosting User Manual

Page	Content
2	Before you start.
3	Planning out your server.
4	Provision Stage with ‘DigitalOcean’ server.
4	Provision Stage with ‘On-Premises’ server.
5	Configuring your DNS
6	Configuring a .well-known
7	Deploy/Update a Server
7	Self-Check
7	Backup Server
7	Start/Restart all Services 
7	Stop all Services
8	Configure Element
8	Configure Jitsi
9	Configure Synapse
10	Setting up Googles ReCaptcha
11	Configure Synapse Admin
11	Configure Website + Access Export
12	Configure Corporal (Advanced)
13	Configure ma1sd (Advanced)
13	Create User
13	Purge Database (Advanced)
14	Purge Media (Advanced)


Before You Start

Some rules you should follow to have a good experience:

1) DO NOT run more then one job template at a time. This could break your server and lead to significant downtime.


Planning Out Your Server

You need to pick URL names for the following:

Base Domain – The base domain for your Matrix service, this could be your existing website or even a subdomain, this URL will appear at the end of your users Matrix IDs. For example: ‘cheesedomain.xyz’ for a user account ‘@billy:cheesedomain.xyz’.

Element Subdomain – The subdomain is where your Element client will appear, this can be any value you like, for example ‘chat’ for an Element client hosted at ‘https://chat.cheesedomain.xyz’.

Base Domain Used – You need to also decide whether to connect this Matrix service to your existing website (Base Domain Used = ‘true’) or whether you would like us to serve the base domain website for you (Base Domain Used = ‘false’) .

Your matrix service will be erected at the ‘matrix’ subdomain, for example:
matrix.cheesedomain.xyz

A Jitsi service will also be erected at the ‘jitsi’ subdomain, for example: 
jisti.cheesedomain.xyz

DigitalOcean Servers

If you’re using a DigitalOcean server the following locations will be available to you:

    • New York City (USA)
    • San Francisco (USA)
    • Amsterdam (NLD)
    • Frankfurt (DEU)
    • Singapore (SGP)
    • London (GBR)
    • Toronto (CAN)
    • Balgalore (IND)

On-Premises Servers

If you plan to bring your own server it needs to have the following properties:

    • x86-64 machine.
    • Debian 10 as the operating system.
    • SSD storage (Preferably NVMe).
    • Public SSH key added to /root/.ssh/authorized_keys
    • A public Ipv4 or Ipv6 address.
    • ~0.5mbps upload per user.


Provision Stage With ‘DigitalOcean’ Server.

Just enter the values you’ve defined after reading the previous page and select your droplet location. A server will be provisioned for you, the job_templates you need to configure it will become available, and DNS advice will be printed for you at the end of the playbook run.

If you receive an error message claiming "Size is not available in this region." consult the droplet availability chart then re-run the provision playbook with another region selected:
https://www.digitalocean.com/docs/platform/availability-matrix/#droplet-plan-availability

If you had your heart set on a specific location contact us and we might be able to help you.


Provision Stage With ‘On-Premises’ Server.

Just enter the values you’ve defined after reading the previous page and enter the Ipv4 and/or Ipv6 address for your server. The on-premises server will be provisioned for you, the job_templates you need to configure it will become available, and DNS advice will be printed for you at the end of the playbook run.


Configuring Your DNS

In the output of provision stage you will receive DNS configuration advice, you must configure this DNS setup or you won’t be able to proceed onto the deploy stage, here is an example of the DNS output:

"msg": [
  "Your server has been created! You now need to configure your DNS to have the",
  "following records:",
  "Type    Host                    Priority  Weight  Port   Target",
  "A       -                       -         -       -      134.209.44.206",
  "A       -                       -         -       -      2604:a880:800:c1::181:7001",
  "A       matrix                  -         -       -      134.209.44.206",
  "A       matrix                  -         -       -      2604:a880:800:c1::181:7001",
  "CNAME   client                  -         -       -      matrix.absolutematrix.com",
  "CNAME   jitsi                   -         -       -      matrix.absolutematrix.com",
  "SRV     _matrix-identity._tcp   10        0       443    matrix.absolutematrix.com",
  "-",
  "Setting the IPv6 record is optional. If you need help doing this please contact us."
]

Here is an example of what the following DNS configuration would look like if entered into NameSilo:


Configuring a .well-known

Note: You only need to configure a .well-known if Base Domain Used = ‘true’

Please follow the steps outlined in: https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/master/docs/configuring-well-known.md

Basically you need to configure 2 files on your base domain:

/.well-known/matrix/server
```
{
	"m.server": "matrix.example.org:8448"
}
```


/.well-known/matrix/client
```
{
	"m.homeserver": {
		"base_url": "https://matrix.example.org"
	}
,
	"m.identity_server": {
		"base_url": "https://matrix.example.org"
	}
}
```


With your base domains URL instead of ‘example.org’.


Deploy/Update a Server

Now that your DNS is configured you can deploy your server. Run the ‘Deploy/Update a Server’ playbook to get started, this playbook is scheduled to update your server every Sunday.


Self-Check

The ‘Self-Check’ playbook allows you to diagnose your server and see metrics for it like how much disk space has filled up and how much CPU/RAM is being utilised.


Backup Server

The ‘Backup Server’ playbook allows you to opt-into an offsite backup. For HIPPA compliance this will need to be enabled. Backups will be run routinely by the AWX administrator.


Start/Restart all Services

Restart or start all the services on your server.


Stop all Services

Stop all the services on your server.


Configure Element

Configures the Element web-client for your server. 

Enable Element-Web		Set if Element web client is enabled or not.

Set Branding for Web Client	Sets the 'branding' seen in the tab and on the welcome page to a custom value.

Set Theme for Web Client	Sets the default theme for the web client, can be changed later by individual users.

Set Welcome Page Background	Set Welcome Page Background

Show Registration Button	If you show the registration button on the welcome page.

Set Element Subdomain		Sets the subdomain of the Element web-client, you should only specify the subdomain, not the base domain you've already set. 
				(Eg: 'element' for element.example.org) Note that if you change this value you'll need to reconfigure your DNS.


Configure Jitsi

Configured the Jitsi instance for your server, this allows you to do group chats and conferencing.

Enable Jitsi		Set if Jitsi is enabled or not. If disabled your server will use the https://jitsi.riot.im server. 
			If you're on a smaller server disabling this might increase the performance of your Matrix service.

Set Default Language	2 digit 639-1 language code to adjust the language of the web client. 
			For a list of possible codes see: https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes


Configure Synapse

Configures Synapse which is your main Matrix server software.

Enable Public Registration		Controls whether people with access to the homeserver can register by themselves.

Enable Federation			Controls whether Synapse will federate at all. Disable this to completely isolate your server from the rest of the Matrix network.

Allow Public Rooms Over Federation	Controls whether remote servers can fetch this server's public rooms directory via federation. For private servers, you'll most likely want to forbid this.

Enable Community Creation		Allows regular users (who aren't server admins) to create 'communities', which are basically groups of rooms.

Enable Synapse Presence			Controls whether presence is enabled. This shows who's online and reading your posts. Disabling it will increase both performance and user privacy.

Enable URL Previews			Controls whether URL previews should be generated. This will cause a request from Synapse to URLs shared by users.

Enable Guest Access			Controls whether 'guest accounts' can access rooms without registering. Guest users do not count towards your servers user limit.

Registration Requires Email		Controls whether an email address is required to register on the server.

Registration Shared Secret		A secret that allows registration of standard or admin accounts by anyone who has the shared secret, even if registration is otherwise disabled. 
					WARNING: You must set a strong and unique password here.

Synapse Max Upload Size			Sets the maximum size for uploaded files in MB.

URL Preview Languages			Sets the languages that URL previews will be generated in. Entries are a 2-3 letter IETF language tag, they must be seperated with newlines. 
					For example: 'fr' https://en.wikipedia.org/wiki/IETF_language_tag

Federation Whitelist			Here you can list the URLs of other Matrix homeservers and Synapse will only federate with those homeservers. 
					Entries must be seperated with newlines and must not have a 'https://' prefix. For example: 'matrix.example.org'

Synapse Auto-Join Rooms			Sets the 'auto-join' rooms, where new users will be automatically invited to, these rooms must already exist. 
					Entries must be room addresses that are separated with newlines. For example: '#announcements:example.org'

Enable ReCaptcha on Registration	Enables Googles ReCaptcha verification for registering an account, recommended for public servers.

Recaptcha Public Key			Sets the Google ReCaptcha public key for this website.

Recaptcha Private Key			Sets the Google ReCaptcha private key for this website.


Setting up Googles ReCaptcha

Navigate to: https://console.cloud.google.com/security/recaptcha/sign-up

Create a Google account, if you haven’t.

Click ‘ENABLE RECAPTCHA ENTERPRISE API’

Click ‘ENABLE’

Click ‘CREATE CREDENTIALS’

From the ‘What API are you using?’ dropdown select ‘reCAPTCHA Enterprise API’

????


Configure Synapse Admin

Configures ‘Synapse Admin’ and administrative tool you can use to manage your server.

Enable Synapse Admin		Set if Synapse Admin is enabled or not. If enabled you can access it at https://matrix.{{ matrix_domain }}/synapse-admin.


Configure Website + Access Export

Configures SFTP access, this can be used to export/import your entire service, as well as configure the web files to be hosted at your base domain. (If you’re hosting it through this platform.)

Customise Base Domain Website		Set if you want to adjust the base domain website using SFTP.

SFTP Authorisation Method		Set whether you want to disable SFTP, use a password to connect to SFTP or connect with a more secure SSH key.

SFTP Password				Sets the password of the 'sftp' account, which allows you to upload a multi-file static website by SFTP, as well as export the latest copy of your Matrix service. 						Must be defined if 'Password' method is selected. WARNING: You must set a strong and unique password here.

SFTP Public SSH Key (More Secure)	Sets the public SSH key used to access the 'sftp' account, which allows you to upload a multi-file static website by SFTP, as well as export the latest copy of your 						Matrix service. Must be defined if 'SSH Key' method is selected.


Configure Corporal (Advanced)

Configures Matrix Corporal, Corporal allows you to define setups of users, rooms and permissions and have the Corporal engine ensure they exist for you. For more information see: https://github.com/devture/matrix-corporal

Enable Corporal				Controls if Matrix Corporal is enabled at all. If you're unsure if you need Matrix Corporal or not, you most likely don't.

Corporal Policy Provider		Controls what provider policy is used with Matrix Corporal.

Simple Static File Configuration	The configuration file for Matrix Corporal, only needed if 'Simple Static File' provider is selected, any configuration entered here will be saved and applied.

HTTP Pull Mode URI			The network address to remotely fetch the configuration from. Only needed if 'HTTP Pull Mode (API Enabled)' provider is selected.

HTTP Pull Mode Authentication Token	An authentication token for pulling the Corporal configuration from a network location. Only needed if 'HTTP Pull Mode (API Enabled)' provider is selected. 
					WARNING: You must set a strong and unique password here.

Corporal API Authentication Token	An authentication token for interfacing with Corporals API. Only needed to be set if 'HTTP Pull Mode (API Enabled)' or 'HTTP Push Mode (API Enabled)' provider is 						selected. WARNING: You must set a strong and unique password here.

Raise Synapse Ratelimits		For Matrix Corporal to work you will need to temporarily raise the rate limits for logins, please return this value to 'Normal' after you're done using Corporal.


Configure ma1sd (Advanced)

ma1sd is your in-built identity server, using it you can connect your Matrix service to an existing identity store (LDAP/AD).

Enable ma1sd			Set if ma1sd is enabled or not. If disabled your server will loose identity functionality (not recommended).

ma1sd Authentication Mode	Set the source of user account authentication credentials with the ma1sd.

LDAP/AD Configuration		Settings for connecting LDAP/AD to the ma1sd service. Ignored if using Synapse Internal, see: https://github.com/ma1uta/ma1sd/blob/master/docs/stores/README.md


Create User

Allows you to create user accounts through AWX, you’ll need to create 1 ‘server admin’ account in order to moderate your service.

Username		Sets the username of the newly created account. Exclude the '@' and server name postfix. So to create @stevo:example.org just enter 'stevo'.

Password		Sets the password of the newly created account.

Administrator Access	Sets whether this user account will be a server admin. Server admins can use their access tokens to run administration/moderation commands on the homeserver.


Purge Database (Advanced)

This template allows you to shrink your Synapse database, it should be used when purging local/remote media doesn’t reclaim enough disk space. Be aware that using this tool can cause cause performance issues and will also cause your server to experience downtime.

Purge Mode		5 modes are available:
			1) No local users [recommended] - Purge rooms with no local users, if you're not sure what mode to use pick this one.
			2) Number of users [slower] - Purge rooms with no local users as well as rooms with more then N users.
			3) Number of events [slower] - Purge rooms with no local users as well as rooms with more then N events.
			4) Skip purging rooms [faster] - Skip purging rooms entirely and just compress other assets within the database.
			5) Perform final shrink - After running one of the above modes, the tool needs to be run again in this mode for your diskspace to be reclaimed. WARNING: This will cause downtime for your Matrix service, it should only be run when you are prepared for that.

Purge Metric Value	The number of users or events used to select rooms for purging, rooms with more users or events then this value will be purged.

Purge Date		The date that rooms will be purged too, the date must be in YYYY-MM-DD format. (Eg: 2020-06-01)


Purge Media (Advanced)

This template allows you to trim your existing media repository, it should be used when your server is running low on disk space. Be aware that deleted local media cannot be recovered.

Media Type		What type of media you would like to purge. Local Media is media that’s generated on your server, it cannot be recovered if deleted. 
			Remote Media is media synced from remote servers you’re federating with, Remote Medias will be resynced as your users attempt to access them.

From Date		The date you would like to purge from in YYYY-MM-DD format. (Eg: 2020-06-23) If you are unsure what date to enter here, just enter the approximate date your service was created.

To Date			The date you would like to purge to in YYYY-MM-DD format. (Eg: 2021-03-27)

