
~~ Setup Wireguard Server ~~

A guide for configuring a wireguard proxy for a Matrix server with networking/firewall issues. The AWX tower will be able to SSH into the wireguard client via port 2222 afterwards and deploy the Matrix server.

1) Create a Debian 10 machine for the wireguard server, it only needs 1GB of RAM. Add the AWX hosts public SSH key to it.


2) Create a Debian 10 machine for the wireguard client. Add the AWX hosts public SSH key to it.


2) Ensure that the 'On-Premises' subscription is already created so you have the subscription_id.


2) Edit users SSH key credential into '00 - Create Wireguard Server' template'. 


3) Run '00 - Create Wireguard Server' template, enter the matrix_domain into the survey.


4) Install wireguard on CLIENT machine:

root@wg-client:# apt update
root@wg-client:# apt install git
root@wg-client:# git clone https://github.com/voidstarzero/wg-ifupdown
root@wg-client:# cd wg-ifupdown
root@wg-client:# ./install.sh

root@wg-client:# echo 'deb http://deb.debian.org/debian buster-backports main' >> /etc/apt/sources.list
root@wg-client:# apt update
root@wg-client:# apt install wireguard/buster-backports


5) Copy wireguard keys over to client machine.

$ scp wireguard.mantismedical.xyz:/etc/wireguard/wg0/client-* ./
client-private.key                                                                            100%   45     0.8KB/s   00:00
client-public.key                                                                             100%   45     0.7KB/s   00:00
$ ssh matrix.mantismedical.xyz mkdir /etc/wireguard/wg0/
$ scp ./client-* matrix.mantismedical.xyz:/etc/wireguard/wg0/
client-private.key                                                                            100%   45    43.8KB/s   00:00
client-public.key                                                                             100%   45    43.0KB/s   00:00
$ ssh matrix.mantismedical.xyz chmod 600 /etc/wireguard/wg0/client-private.key


6) On the wireguard client adjust '/etc/network/interfaces.d/wg0' file:

```
auto wg0
iface wg0 inet static
#    maybe? # pre-up /sbin/modprobe wireguard
    wg-private-key /etc/wireguard/wg0/client-private.key
    wg-listen-port 51820
    wg-fwmark 42
    address 192.168.99.2/24
#    wg-config-file /etc/wireguard/wg0/config
#    wg-config-file /etc/wireguard/example-peers.conf
    wg-autoroute no
#    wg-addroute 198.51.100.0/24
#    wg-addroute 203.0.113.0/24
# see https://www.wireguard.com/netns/#improved-rule-based-routing
    post-up ip route add default dev wg0 table 2468
    post-up ip rule add not fwmark 42 table 2468
    post-up ip rule add table main suppress_prefixlength 0
```


7) On the wireguard client adjust '/etc/wireguard/wg0/config' file, include content of the servers public key as well as the public IP:

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


8) Install Linux headers for wireguard module on the client machine:

root@wg-client:# uname -r
4.19.0-17-amd64
root@wg-client:# apt install linux-headers-4.19.0-17-amd64


9) CHECK IF IT'S WORKING!

root@wg-client:# modprobe wireguard

root@wg-client:# ifdown wg0;ifup wg0

root@wg-client:# wg show
interface: wg0
  public key: bAsgRIuBJXXVlQfu3c8NNMtlWtsZQOVSH0xtQw58Znk=
  private key: (hidden)
  listening port: 51820

peer: Bw1E9jTMv5c5HlEqTFm3EIdn+Fh5MmQYa7yXI2pv2H4=
  endpoint: 128.199.193.165:51820
  allowed ips: 0.0.0.0/0, ::/0
  latest handshake: 5 seconds ago
  transfer: 732 B received, 788 B sent

root@matrix:~# ping 192.168.99.1
PING 192.168.99.1 (192.168.99.1) 56(84) bytes of data.
64 bytes from 192.168.99.1: icmp_seq=1 ttl=64 time=54.0 ms
64 bytes from 192.168.99.1: icmp_seq=2 ttl=64 time=54.7 ms

