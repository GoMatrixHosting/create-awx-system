#!/usr/bin/python3

import json
import os
import subprocess

with open(os.environ['HOOK_PAYLOAD'], "r") as f:
  # returns JSON object as a dictionary
  # If the data being deserialized is not a valid JSON document, a JSONDecodeError will be raised
  data = json.load(f)

def shellcmd(command):
  print(command)
  rc = subprocess.run(command, universal_newlines=True, capture_output=True)
  print(rc.returncode)
  print(rc.stdout)
  print(rc.stderr)
  return(rc)

#########################################
# Hard Coded AWX/Tower Credentials          #
create_subscription_job_template = "00 - Ansible Create MP Subscription"
delete_subscription_job_template = "00 - Ansible Delete Subscription"
#########################################

#print(data)
print(json.dumps(data, indent = 1))

#shellcmd(["awx-cli", "config", "host", str(awx_host)])
#shellcmd(["awx-cli", "config", "username", str(awx_username)])
#shellcmd(["awx-cli", "config", "password", str(awx_password)])

# Launch Tower Job Template Example
# $ awx-cli job launch -J "00 - Create Subscription" --monitor --extra-vars='first_name="Freddy" last_name="Kreuger" email="user@example.com" subscr_id="mp-sub-5f83bf681654b" plan_title="Medium Server"'

event_type = str(data['event'])
print("Event type is: " + event_type)

if event_type == "recurring-transaction-completed":
  plan_title = str(data['data']['membership']['title'])
  print("Plan selected: " + data['data']['membership']['title'])
  subscription_id = str(data['data']['subscription']['subscr_id'])
  print("Subscription ID: " + subscription_id)
  member_id = str(data['data']['member']['id'])
  print("Member ID: " + member_id)
  client_email = str(data['data']['member']['email'])
  print("Client email is: " + client_email)
  client_first_name = str(data['data']['member']['first_name'])
  print("Clients first name is: " + client_first_name)
  client_last_name = str(data['data']['member']['last_name'])
  print("Clients last name is:  " + client_last_name)
  awx_job_launch_command = ["awx-cli", "job", "launch", "-J", create_subscription_job_template]
  # passing extra_vars requires AWX's "PROMPT ON LAUNCH" to be enabled
  extra_vars = {}
#  client_first_name="Robert'); DROP TABLE Students; override --"; client_last_name='Sploits-override'
  extra_vars['client_first_name']=client_first_name
  extra_vars['client_last_name']=client_last_name
  extra_vars['client_email']=client_email
  extra_vars['subscription_id']=subscription_id
  extra_vars['member_id']=member_id
  extra_vars['plan_title']=plan_title
  extravars = '--extra-vars=' + json.JSONEncoder().encode(extra_vars)
  awx_job_launch_command = awx_job_launch_command + [ extravars ]
  shellcmd(awx_job_launch_command)

# need to add 'delete-subscription' tag to this:

elif event_type == "subscription-expired":
  subscription_id = str(data['data']['subscr_id'])
  print("Subscription ID: " + subscription_id)
  member_id = str(data['data']['member']['id'])
  print("Member ID: " + member_id)

  extra_vars = {}
  extra_vars['subscription_id']=subscription_id
  extra_vars['member_id']=member_id
  awx_job_launch_command = ["awx-cli", "job", "launch", "-J", delete_subscription_job_template]
  # passing extra_vars requires AWX's "PROMPT ON LAUNCH" to be enabled
  extravars = '--extra-vars=' + json.JSONEncoder().encode(extra_vars)
  awx_job_launch_command = awx_job_launch_command + [ extravars ]
  shellcmd(awx_job_launch_command)

# Notes on direct python method:
  #awx_job_launch_command = ["curl", "-H", "Host: 127.0.0.1:8080", "-H", 'Authorization: Bearer xxOAUTH_TOKENxx', '-H', 'Content-Type: application/json' ]
  # curl, OAUTH: awx_job_launch_command = ["curl", "-H", "Host: 127.0.0.1:8080", "-H", 'Authorization: Bearer xxOAUTH_TOKENxx', '-H', 'Content-Type: application/json' ]
  # curl, Basic auth: wx_job_launch_command = ["curl", "-H", "Host: 127.0.0.1:8080", "-H", 'Authorization: Basic XXXX=', '-H', 'Content-Type: application/json' ]
  # extravars = '"{\"extra_vars\": \"{\\\"client_email\\\": \\\"jayfoo@example.com\\\", \\\"client_first_name\\\": \\\"Jay\\\", \\\"client_last_name\\\": \\\"Foo\\\", \\\"subscription_id\\\": \\\"I-MLNR0UVM62NU\\\", \\\"plan_title\\\": \\\"Medium Server\\\"}\"}"
  # extra_vars = '{"extra_vars": "{\"client_email\": \"jayfoo@example.com\", \"client_first_name\": \"Jay\", \"client_last_name\": \"Foo\", \"subscription_id\": \"I-MLNR0UVM62NU\", \"plan_title\": \"Medium Server\"}"}'
