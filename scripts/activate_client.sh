#!/bin/bash

# Activate wireless client mode

/usr/bin/systemctl stop hostapd
if [[ $? -ne 0  ]] ; then
    echo "Failed to stop hostapd"
fi

/usr/bin/systemctl stop dnsmasq
if [[ $? -ne 0  ]] ; then
    echo "Failed to stop dnsmasq"
fi

/usr/bin/systemctl start wpa_supplicant
if [[ $? -ne 0  ]] ; then
    echo "Failed to start wpa_supplicant"
fi

/usr/sbin/ifup wlan0
if [[ $? -ne 0  ]] ; then
    echo "Failed to set wlan0 interface up"
fi

/bin/ip link set wlan0 mode default
if [[ $? -ne 0  ]] ; then
    echo "Failed to set wlan0 interface mode to default"
fi

echo "Wireless client mode activated successfully"
