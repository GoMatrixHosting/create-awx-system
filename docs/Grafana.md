
# Extra steps to setup Grafana

1) Import Dashboards:

https://monitor.example.org/dashboard/import
Click 'Upload JSON file' > Select the /graphana/synapse.json file from this repo
Select prometheus source 'local_prometheus' > Click 'Import'

Also import this template using 'Upload JSON file': 
Click 'Upload JSON file' > Select the /graphana/node-exporter-full.json file from this repo
Select prometheus source 'local_prometheus' > Click 'Import'

2) Set 'Access' on Prometheus Data Source:

https://monitor.example.org/datasources/edit/1/
HTTP > Access > Select “Server (default)” from dropdown menu.
Click 'Save & Test' at the bottom.

3) https://monitor.example.org/d/rYdddlPWk/node-exporter-full
Save icon
Add changelog note, tick to save variables as dashboard default.
