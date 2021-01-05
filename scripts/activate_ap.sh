#!/bin/bash

# Activate the software access point (AP)

/usr/bin/systemctl stop wpa_supplicant
wpa=$?

/usr/sbin/ifdown wlan0
ifdown=$?

/usr/bin/systemctl unmask hostapd
unmask=$?

/usr/bin/systemctl start hostapd
hostapd=$?

/usr/bin/systemctl start dnsmasq
dnsmasq=$?

if [[ "$wpa" -ne 0  ]] ; then
    echo "Failed to stop wpa_supplicant"
    exit 1
elif [[ "$ifdown" -ne 0 ]] ; then
    echo "Failed to set wlan0 down"
    exit 1
elif [[ "$unmask" -ne 0 ]] ; then
    echo "Failed to unmask hostapd"
    exit 1
elif [[ "$hostapd" -ne 0 ]] ; then
    echo "Failed to start hostapd"
    exit 1
elif [[ "$dnsmasq" -ne 0 ]] ; then
    echo "Failed to start dnsmasq"
    exit 1
else
    echo "Access point activated successfully"
    exit 0
fi
