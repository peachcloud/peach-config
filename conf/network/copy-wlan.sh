#!/bin/bash

FILE=/boot/firmware/wpa_supplicant.conf
if test -f "$FILE"; then
    cp /boot/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant-wlan0.conf
    chown root:netdev /etc/wpa_supplicant/wpa_supplicant-wlan0.conf
    rm /boot/firmware/wpa_supplicant.conf
fi