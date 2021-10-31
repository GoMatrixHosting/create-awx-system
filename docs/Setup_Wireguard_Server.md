
~~ Setup Wireguard Server ~~

A guide for configuring a wireguard proxy for a Matrix server with networking/firewall issues. The AWX tower will be able to SSH into the wireguard client via port 2222 afterwards and deploy the Matrix server.

1) Create a Debian 10/11 machine for the wireguard server, it only needs 1GB of RAM. Add the AWX clients public SSH key to it.


2) Create a Debian 10/11 machine for the wireguard client. Add the AWX clients public SSH key to it.


3) Ensure that the 'On-Premises' subscription is already created so you have the subscription_id.


4) Edit users SSH key credential into '00 - Create Wireguard Server' template'. 


5) Run '00 - Create Wireguard Server' template, enter these details into the survey:
matrix_domain
server_ip
server_size
member_id
subscription_id


6) Install wireguard on CLIENT machine:

root@wg-client:# apt update
root@wg-client:# apt install git
root@wg-client:# git clone https://github.com/voidstarzero/wg-ifupdown
root@wg-client:# cd wg-ifupdown
root@wg-client:# ./install.sh

# For Debian 10:
root@wg-client:# echo 'deb http://deb.debian.org/debian buster-backports main' >> /etc/apt/sources.list
root@wg-client:# apt update
root@wg-client:# apt install wireguard/buster-backports

# For Debian 11:
root@wg-client:# apt install wireguard


7) Copy wireguard keys over to client machine.

$ scp wireguard.mantismedical.xyz:/etc/wireguard/wg0/client-* ./
client-private.key                                                                            100%   45     0.8KB/s   00:00
client-public.key                                                                             100%   45     0.7KB/s   00:00
$ ssh matrix.mantismedical.xyz mkdir /etc/wireguard/wg0/
$ scp ./client-* matrix.mantismedical.xyz:/etc/wireguard/wg0/
client-private.key                                                                            100%   45    43.8KB/s   00:00
client-public.key                                                                             100%   45    43.0KB/s   00:00
$ ssh matrix.mantismedical.xyz chmod 600 /etc/wireguard/wg0/client-private.key


8) On the wireguard client adjust '/etc/network/interfaces.d/wg0' file:

```
auto wg0
iface wg0 inet static
#    maybe? # pre-up /sbin/modprobe wireguard
    wg-private-key /etc/wireguard/wg0/client-private.key
    wg-listen-port 51820
    wg-fwmark 42
    address 192.168.99.2/24
    wg-autoroute no
# see https://www.wireguard.com/netns/#improved-rule-based-routing
    post-up ip route add default dev wg0 table 2468
    post-up ip rule add not fwmark 42 table 2468
    post-up ip rule add table main suppress_prefixlength 0
```


9) On the wireguard client adjust '/etc/wireguard/wg0/config' file, include content of the servers public key as well as the public IP:

$ ssh wireguard.mantismedical.xyz cat /etc/wireguard/wg0/server-public.key
JWFWfaUESFw5KDbwFzPTESiUIfall6n8wciluxJaI0o=

``` 
[Peer]
# external wireguard relay server
Endpoint = 165.22.245.207:51820
PublicKey = JWFWfaUESFw5KDbwFzPTESiUIfall6n8wciluxJaI0o=
#peer is a relay server that bounces all internet & VPN traffic (like a proxy), including IPv6
AllowedIPs = 0.0.0.0/0,::/0
#AllowedIPs = 192.168.99.1/32
PersistentKeepalive = 25
```


10) CHECK IF IT'S WORKING!

root@wg-client:# ifup wg0

root@wg-client:# wg show
interface: wg0
  public key: hF3p/hI1vMmE7QX+d1IqgzLp/eqimrhIQCcuATXKJTc=
  private key: (hidden)
  listening port: 51820
  fwmark: 0x2a

peer: 0chY4Rel4oCcrQSIPckJQ01q8Ah8GNSGL5zBftaFy2I=
  endpoint: 165.22.245.207:51820
  allowed ips: 0.0.0.0/0, ::/0
  latest handshake: 25 seconds ago
  transfer: 92 B received, 180 B sent
  persistent keepalive: every 25 seconds

root@matrix:~# ping 192.168.99.1
PING 192.168.99.1 (192.168.99.1) 56(84) bytes of data.
64 bytes from 192.168.99.1: icmp_seq=1 ttl=64 time=54.0 ms
64 bytes from 192.168.99.1: icmp_seq=2 ttl=64 time=54.7 ms


12) Remove the 'setup-firewall' tag then run 'Provision a New Server', enter the external IP of the wireguard server into the survey. 


