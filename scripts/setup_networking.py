# setup_networking.py

# Standalone script to configure a Debian installation to use
# systemd-networkd for general networking. The script configures the eth0,
# wlan0 and ap0 interfaces. This configuration allows switching between
# wireless client mode (wlan0) and wireless access point mode (ap0)

import os
import subprocess

print("[ INSTALLING SYSTEM REQUIREMENTS ]")
subprocess.call(["apt", "install", "libnss-resolve"])

print("[ DEINSTALLING CLASSIC NETWORKING ]")
subprocess.call(["apt",
                 "--autoremove",
                 "purge",
                 "ifupdown",
                 "dhcpcd5",
                 "isc-dhcp-client",
                 "isc-dhcp-common",
                 "rsyslog"])
subprocess.call(["apt-mark",
                 "hold",
                 "ifupdown",
                 "dhcpcd5",
                 "isc-dhcp-client",
                 "isc-dhcp-common",
                 "rsyslog",
                 "openresolv"])
subprocess.call(["rm", "-r", "/etc/network", "/etc/dhcp"])

print("[ SETTING UP SYSTEMD-RESOLVED & SYSTEMD-NETWORKD ]")
subprocess.call(["apt", "--autoremove", "purge", "avahi-daemon"])
subprocess.call(["apt-mark", "hold", "avahi-daemon", "libnss-mdns"])
subprocess.call(
    ["ln", "-sf", "/run/systemd/resolve/stub-resolv.conf", "/etc/resolv.conf"])
subprocess.call(["systemctl",
                 "enable",
                 "systemd-networkd.service",
                 "systemd-resolved.service"])

print("[ CREATING INTERFACE FILE FOR WIRED CONNECTION ]")
subprocess.call(["cp", "conf/network/04-wired.network",
                "/etc/systemd/network/04-wired.network"])

# might need to reboot here...

print("[ SETTING UP WPA_SUPPLICANT AS WIFI CLIENT WITH WLAN0 ]")
subprocess.call(["cp", "conf/network/wpa_supplicant-wlan0.conf",
                "/etc/wpa_supplicant/wpa_supplicant-wlan0.conf"])
subprocess.call([
    "chmod",
    "600",
    "/etc/wpa_supplicant/wpa_supplicant-wlan0.conf"])
subprocess.call(["systemctl", "disable", "wpa_supplicant.service"])
subprocess.call(["systemctl", "enable", "wpa_supplicant@wlan0.service"])

print("[ SETTING UP WPA_SUPPLICANT AS ACCESS POINT WITH AP0 ]")
subprocess.call(["cp", "conf/network/wpa_supplicant-ap0.conf",
                "/etc/wpa_supplicant/wpa_supplicant-ap0.conf"])
subprocess.call(["chmod", "600", "/etc/wpa_supplicant/wpa_supplicant-ap0.conf"])

print("[ CONFIGURING INTERFACES ]")
subprocess.call(["cp", "conf/network/08-wlan0.network",
                "/etc/systemd/network/08-wlan0.network"])
subprocess.call(["cp", "conf/network/12-ap0.network",
                "/etc/systemd/network/12-ap0.network"])

print("[ MODIFYING SERVICE FOR ACCESS POINT TO USE AP0 ]")
subprocess.call(["systemctl", "disable", "wpa_supplicant@ap0.service"])
subprocess.call(["cp", "conf/network/wpa_supplicant@ap0.service",
                "/etc/systemd/system/wpa_supplicant@ap0.service"])

print("[ SET WLAN0 TO RUN AS CLIENT ON STARTUP ]")
subprocess.call(["systemctl", "enable", "wpa_supplicant@wlan0.service"])
subprocess.call(["systemctl", "disable", "wpa_supplicant@ap0.service"])

print("[ NETWORKING HAS BEEN CONFIGURED ]")
print("[ ------------------------------ ]")
print("[ please reboot your device now. ]")
