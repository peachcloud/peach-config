#!/bin/bash

# Activate wireless client mode
echo "Stopping hostapd"
/usr/bin/systemctl stop hostapd
echo "Stopping dnsmasq"
/usr/bin/systemctl stop dnsmasq
echo "Starting wpa_supplicant"
/usr/bin/systemctl start wpa_supplicant
echo "Setting wlan0 interface up"
/usr/sbin/ifup wlan0
echo "Setting wlan0 to default mode"
/bin/ip link set wlan0 mode default
