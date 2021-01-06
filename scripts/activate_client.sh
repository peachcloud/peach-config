#!/bin/bash

# Activate wireless client mode

/usr/bin/systemctl stop hostapd
hostapd=$?

/usr/bin/systemctl stop dnsmasq
dnsmasq=$?

/usr/bin/systemctl start wpa_supplicant
wpa=$?

/usr/sbin/ifup wlan0
ifup=$?

/bin/ip link set wlan0 mode default
mode=$?

if [[ "$hostapd" -ne 0  ]] ; then
    echo "Failed to stop hostapd"
    exit 1
elif [[ "$dnsmasq" -ne 0 ]] ; then
    echo "Failed to stop dnsmasq"
    exit 1
elif [[ "$wpa" -ne 0 ]] ; then
    echo "Failed to start wpa_supplicant"
    exit 1
elif [[ "$ifup" -ne 0 ]] ; then
    echo "Failed to set wlan0 up"
    exit 1
elif [[ "$mode" -ne 0 ]] ; then
    echo "Failed to set wlan0 mode to default"
    exit 1
else
    echo "Wireless client mode activated successfully"
    exit 0
fi
