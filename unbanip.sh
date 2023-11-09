#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root." 
   exit 1
fi

if [ -z "$1" ]; then
    echo "Usage: $0 <ip_address>"
    exit 1
fi

IP=$1
iptables -D INPUT -s $IP -j DROP

echo "Unblocked IP address $IP from iptables."