#!/bin/bash

# Activate the software access point (AP)

/usr/bin/systemctl stop wpa_supplicant
if [[ $? -ne 0  ]] ; then
    echo "Failed to stop wpa_supplicant"
fi

/usr/sbin/ifdown wlan0
if [[ $? -ne 0  ]] ; then
    echo "Failed to set wlan0 interface down"
fi

/usr/bin/systemctl unmask hostapd
if [[ $? -ne 0  ]] ; then
    echo "Failed to unmask hostapd"
fi

/usr/bin/systemctl start hostapd
if [[ $? -ne 0  ]] ; then
    echo "Failed to start hostapd"
fi

/usr/bin/systemctl start dnsmasq
if [[ $? -ne 0  ]] ; then
    echo "Failed to start dnsmasq"
fi

echo "Access point activated successfully"
