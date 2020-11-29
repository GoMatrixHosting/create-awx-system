
# Extra steps to setup Grafana

1) Import Dashboards:

https://monitor.example.org/dashboard/import
Import via grafana.com > Enter "1860" > Click 'Load'

Also import this template using 'Upload JSON file': 
https://raw.githubusercontent.com/matrix-org/synapse/master/contrib/grafana/synapse.json

2) Set 'Access' on Prometheus Data Source:

https://monitor.example.org/datasources/edit/1/
HTTP > Access > Select “Server (default)” from dropdown menu.
Click 'Save & Test' at the bottom.

3) Are these really needed?
http://192.168.1.173:3000/d/000000012/synapse-matrix-perthchat-org?orgId=1&editview=dashboard_json
→ Copy

https://monitor.example.org/dashboard/import
→ Paste
Customise name, UID “synapse”
Save
Produces permlink:
https://monitor.example.org/d/synapse/synapse (??)

https://monitor.example.org/d/rYdddlPWk/node-exporter-full
Save icon
Add changelog note, tick to save as default (??)
