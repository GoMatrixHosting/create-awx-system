import sys
import json
import subprocess
from pathlib import Path

def shellcmd(command):
  print(command)
  rc = subprocess.run(command, universal_newlines=True, capture_output=True)
  print(rc.returncode)
  print(rc.stdout)
  print(rc.stderr)
  return(rc)

print(sys.argv[1])
input = sys.argv[1]
client_email = ""

# Example input:
# "{"log":"2021-01-20 15:13:05,392 INFO     awx.api.generics User billyjean@protonmail.com logged in from 172.18.0.1\n","stream":"stderr","time":"2021-01-20T15:13:05.393360698Z"}"

# trim email out of the input

split_input = input.split()

for entry in split_input:
  if "@" in entry:
    client_email = entry

print("client_email is: " + client_email)

if len(client_email) == 0:
  print("Client email not found! Exiting...")
  sys.exit()

# check client-file for that email

client_file_path = "/var/lib/awx/projects/clients/client-list"
client_file = open(client_file_path,'r')
client_file_contents = client_file.read()
client_file.close()

# if it has ',binded' on the end, exit gracefully

client_file_contents_lines = client_file_contents.split("\n")
for line in client_file_contents_lines:
  if (client_email in line) and (",bound" in line):
    print("This user account is already bound. Exiting...")
    sys.exit()
  elif (client_email in line) and (",bound" not in line):
    member_id = line.split(',')[0]

print("Member_id is: " + member_id)

# Touch the extra-vars file
Path('/tmp/bind_user.json').touch()
 
# Clear the extra-vars file
open('/tmp/bind_user.json', 'w').close()
  
# Write the extra-vars file
extra_vars_json = {"member_id": member_id, "client_email": client_email}
with open('/tmp/bind_user.json', 'w') as extra_vars_file:
  json.dump(extra_vars_json, extra_vars_file)
extra_vars_file.close()

# Launch the ansible playbook
ansible_launch_command = ["/usr/bin/ansible-playbook", "-v", "/usr/local/bin/bind-user.yml"]
shellcmd(ansible_launch_command)

# if it does not, bind that user to the team, then add ',binded' to the end of that line

new_client_file_contents = client_file_contents.replace(client_email, (client_email + ",bound"))

client_file = open(client_file_path,'w')
client_file.write(new_client_file_contents)
client_file.close()
