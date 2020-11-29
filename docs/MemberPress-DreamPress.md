
# Setting up 'DreamPress'

1) https://panel.dreamhost.com/

WordPress > Managed WordPress > 'Manage' for your site > Domain tab > 'Import Existing Site'

LOOKS GOOD! :)

EXTRA CONFIG:

2) Adjust webhook target in WP-Admin > MemberPress > Developer > Webhooks

Seems to be done :O (fuck that was easy!)


# Wordpress Plugins Used

- GP Premium
- MemberPress Developer Tools
- MemberPress Plus
- Proxy Cache Purge
- WP OAuth Server


# Paypal Sandbox Configuration

1) Create a business and personal account for the sandbox.paypal.com site, first login to developer.paypal.com with your real account. Then click 'Sandbox' > 'Accounts' in the left column.

2) Login with sandbox business credentials to: https://www.sandbox.paypal.com/businessmanage/credentials/apiaccess, in the 'NVP/SOAP API integration (Classic)' section click 'Manage API Credentials'. Copy the API username, API password, Signature into the MemberPress PayPal settings. (Check 'Advanced mode.)

3) Also copy business sandbox account email into MemberPress PayPal settings.

4) Click 'Update Options' in MemberPress PayPal settings.

5) Copy the PayPal IPN settings value from MemberPress PayPal settings into 'https://www.sandbox.paypal.com/businessmanage/account/website' > 'Website payments' > 'Instant payment notifications' > 'Choose IPN Settings' > then enter the IPN URL from Memberpress and check 'Recieve IPN messages (Enabled), then click 'Save'.

6) 'https://www.sandbox.paypal.com/businessmanage/account/website' > 'Website payments' > 'Website preferences' > check 'On' for 'Auto return', then copy the 'Return URL' from MemberPress Payment settings.

7) In the same page make sure 'Payment data transfer' is 'On'. And that 'Encrypted website payments' is 'Off'. And that 'PayPal account optional' is 'Off'.

The PayPal sandbox should be configured properly now!

8) Back to developer.paypal.com, create a personnal sandbox account for testing.

9) Open a private window and attempt to purchase a membership with the personnal sandbox account.


