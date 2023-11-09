#!/bin/bash

echo "Banned IPs using iptables:"

banned_ips=$(sudo iptables -L -n | awk '/DROP/{print $4}')

if [ -z "$banned_ips" ]; then
    echo "No IPs are currently banned."
else
    for ip in $banned_ips; do
        rule=$(sudo iptables -L -n --line-numbers | awk -v ip="$ip" '$0 ~ ip {print $1}')
        echo "IP: $ip - Rule Number: $rule"
    done
fi
