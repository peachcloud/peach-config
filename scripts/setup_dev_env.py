# setup_dev_env.py

# Install and configure development environment for PeachCloud on RPi3 with Debian Buster
# Includes installation of Rust and setup of I2C and a RTC
# Consult the PeachCloud GPIO documentation [ ... ] for pinouts

import os
import subprocess
import sys
import argparse

# Setup argument parser
parser = argparse.ArgumentParser()
parser.add_argument("user", type=str, help="username for the default user account")
parser.add_argument("-i", "--i2c", help="configure i2c", action="store_true")
parser.add_argument("-r", "--rtc", choices=["ds1307", "ds3231"], help="configure real-time clock")
args = parser.parse_args()

# Save username argument
username = args.user

# Update Pi and install requirements
print("[ UPDATING OPERATING SYSTEM ]")
subprocess.call(["apt-get", "update", "-y"])
subprocess.call(["apt-get", "upgrade", "-y"])
print("[ INSTALLING SYSTEM REQUIREMENTS ]")
subprocess.call(["apt-get", "install", "vim", "man-db", "locales", "iw", "hostapd", "dnsmasq", "git", "python-smbus", "i2c-tools", "build-essential", "curl", "mosh", "sudo", "pkg-config", "libssl-dev", "avahi-daemon", "nginx", "wget", "-y"])

# Add the system user with supplied username
print("[ ADDING SYSTEM USER ]")
subprocess.call(["/usr/sbin/adduser", username])

# Overwrite configuration files
subprocess.call(["mkdir", "/boot/firmware/overlays/"])
subprocess.call(["cp", "conf/mygpio.dtbo", "/boot/firmware/overlays/mygpio.dtbo"])
subprocess.call(["cp", "conf/config.txt", "/boot/firmware/config.txt"])
subprocess.call(["cp", "conf/modules", "/etc/modules"])
subprocess.call(["cp", "conf/peach.conf", "/etc/nginx/sites-available/peach.conf"])
subprocess.call(["ln", "-s", "/etc/nginx/sites-available/peach.conf", "/etc/nginx/sites-enabled/"])
subprocess.call(["cp", "conf/hostname", "/etc/hostname"])
subprocess.call(["cp", "conf/hosts", "/etc/hosts"])
subprocess.call(["cp", "conf/interfaces", "/etc/network/interfaces"])
subprocess.call(["cp", "conf/hostapd", "/etc/default/hostapd"])
subprocess.call(["cp", "conf/hostapd.conf", "/etc/hostapd/hostapd.conf"])
subprocess.call(["cp", "conf/dnsmasq.conf", "/etc/dnsmasq.conf"])
subprocess.call(["cp", "conf/dhcpd.conf", "/etc/dhcpd.conf"])
subprocess.call(["cp", "conf/00-accesspoint.rules", "/etc/udev/rules.d/00-accesspoint.rules"])
subprocess.call(["cp", "conf/activate-rtc.service", "/etc/systemd/system/activate-rtc.service"])

# left out: setting of locales, rust installation, console log-level printing

# we might also eventually want to pull the `.deb` release files for all microservices and install them. work towards an all-in-one installation script with optional flags to selectively install either the dev environment (will include rust) or a release environment (no rust or other bells and whistles)

#subprocess.call(["sysctl", "-w", "kernel.printk='4 4 1 7'"])
