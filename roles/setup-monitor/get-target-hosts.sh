
#!/bin/bash

echo 'matrix.perthchat.org'
curl --silent --user admin:{{ awx_admin_password }} https://{{ awx_url }}/api/v2/hosts/ |
	jq .results[].name |
	sort -u |
	tr -d '"\\' |
	egrep -v "dummyvalue|example\.com"
