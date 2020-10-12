#!/bin/bash

# Activate the software access point (AP)
echo "Stopping wpa_supplicant"
/usr/bin/systemctl stop wpa_supplicant
echo "Setting wlan0 interface down"
/usr/sbin/ifdown wlan0
echo "Starting hostapd"
/usr/bin/systemctl start hostapd
echo "Starting dnsmasq"
/usr/bin/systemctl start dnsmasq
