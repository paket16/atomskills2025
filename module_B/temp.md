#!/bin/bash 
echo -e "conn vpn
auto=start
type=tunnel
authby=secret
left=200.20.20.10
right=100.10.10.10
leftsubnet=0.0.0.0/0
rightsubnet=0.0.0.0/0leftprotoport=gre
rightprotoport=gre
ike=aes128-sha256-modp3072
esp=aes128-sha256" >> /etc/ipsec.conf





conn vpn
auto=start
type=tunnel
authby=secret
left=200.20.20.10
right=100.10.10.10
leftsubnet=0.0.0.0/0
rightsubnet=0.0.0.0/0
leftprotoport=gre
rightprotoport=gre
ike=aes128-sha256-modp3072
esp=aes128-sha256