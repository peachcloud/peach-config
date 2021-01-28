# setup_networking.py

# Standalone script to configure a Debian installation to use
# systemd-networkd for general networking. The script configures the eth0,
# wlan0 and ap0 interfaces. This configuration allows switching between
# wireless client mode (wlan0) and wireless access point mode (ap0)

import subprocess
import os


def configure_networking():

    print("[ INSTALLING SYSTEM REQUIREMENTS ]")
    subprocess.call(["apt", "install", "-y", "libnss-resolve"])

    print("[ SETTING HOST ]")
    subprocess.call(["cp", "conf/hostname", "/etc/hostname"])
    subprocess.call(["cp", "conf/hosts", "/etc/hosts"])

    print("[ DEINSTALLING CLASSIC NETWORKING ]")
    subprocess.call(["apt-get",
                     "autoremove",
                     "-y",
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
    subprocess.call(["rm", "-rf", "/etc/network", "/etc/dhcp"])

    print("[ SETTING UP SYSTEMD-RESOLVED & SYSTEMD-NETWORKD ]")
    subprocess.call(["apt-get", "--autoremove", "avahi-daemon"])
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

    print("[ SETTING UP WPA_SUPPLICANT AS WIFI CLIENT WITH WLAN0 ]")
    # to avoid overwriting previous credentials, only copy file if it doesn't already exist
    if not os.path.exists("/etc/wpa_supplicant/wpa_supplicant-wlan0.conf"):
        subprocess.call(["cp", "conf/network/wpa_supplicant-wlan0.conf",
                         "/etc/wpa_supplicant/wpa_supplicant-wlan0.conf"])
    subprocess.call([
        "chmod",
        "660",
        "/etc/wpa_supplicant/wpa_supplicant-wlan0.conf"])
    subprocess.call(["chown", "root:netdev", "/etc/wpa_supplicant/wpa_supplicant-wlan0.conf"])
    subprocess.call(["systemctl", "disable", "wpa_supplicant.service"])
    subprocess.call(["systemctl", "enable", "wpa_supplicant@wlan0.service"])

    print("[ SETTING UP WPA_SUPPLICANT AS ACCESS POINT WITH AP0 ]")
    subprocess.call(["cp", "conf/network/wpa_supplicant-ap0.conf",
                     "/etc/wpa_supplicant/wpa_supplicant-ap0.conf"])
    subprocess.call(
        ["chmod", "600", "/etc/wpa_supplicant/wpa_supplicant-ap0.conf"])

    print("[ CONFIGURING INTERFACES ]")
    subprocess.call(["cp", "conf/network/08-wlan0.network",
                     "/etc/systemd/network/08-wlan0.network"])
    subprocess.call(["cp", "conf/network/12-ap0.network",
                     "/etc/systemd/network/12-ap0.network"])

    print("[ MODIFYING SERVICE FOR ACCESS POINT TO USE AP0 ]")
    subprocess.call(["systemctl", "disable", "wpa_supplicant@ap0.service"])
    subprocess.call(["cp", "conf/network/wpa_supplicant@ap0.service",
                     "/etc/systemd/system/wpa_supplicant@ap0.service"])

    print("[ SETTING WLAN0 TO RUN AS CLIENT ON STARTUP ]")
    subprocess.call(["systemctl", "enable", "wpa_supplicant@wlan0.service"])
    subprocess.call(["systemctl", "disable", "wpa_supplicant@ap0.service"])

    print("[ NETWORKING HAS BEEN CONFIGURED ]")


if __name__ == '__main__':

    configure_networking()

    print("[ ------------------------------ ]")
    print("[ please reboot your device now. ]")
