
# Extra steps to setup Grafana

1) Import Dashboards:

https://monitor.example.org/dashboard/import
Import via grafana.com > Enter "1860" > Click 'Load'
Select prometheus source 'local_prometheus' > Click 'Import'

Also import this template using 'Upload JSON file': 
https://raw.githubusercontent.com/matrix-org/synapse/master/contrib/grafana/synapse.json
Change the 'Unique Identifier' to equal 'synapse'.
Select prometheus source 'local_prometheus' > Click 'Import'

2) Set 'Access' on Prometheus Data Source:

https://monitor.example.org/datasources/edit/1/
HTTP > Access > Select “Server (default)” from dropdown menu.
Click 'Save & Test' at the bottom.

3) https://monitor.example.org/d/rYdddlPWk/node-exporter-full
Save icon
Add changelog note, tick to save variables as dashboard default.
