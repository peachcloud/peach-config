# setup_dev_env.py

# Install and configure development environment for PeachCloud on RPi3 with Debian Buster
# Includes installation of Rust and setup of I2C and a RTC
# Consult the PeachCloud GPIO documentation [ ... ] for pinouts

import os
import subprocess
import sys


# Save arguments
username = sys.argv[1]

# Update Pi and install requirements
subprocess.call(["apt-get", "update", "-y"])
subprocess.call(["apt-get", "upgrade", "-y"])
subprocess.call(["apt-get", "install", "vim", "man-db", "locales", "iw", "hostapd", "dnsmasq", "git", "python-smbus", "i2c-tools", "build-essential", "curl", "mosh", "sudo", "pkg-config", "libssl-dev", "avahi-daemon", "-y"])
subprocess.call(["/usr/sbin/adduser", username])

# Overwrite configuration files
subprocess.call(["cp", "conf/bcm2710-rpi-3-b.dtb", "/boot/firmware/bcm2710-rpi-3-b.dtb"])
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
