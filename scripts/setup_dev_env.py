# setup_dev_env.py

# Install and configure development environment for PeachCloud on RPi3 with Debian Buster
# Includes installation of Rust and setup of I2C and a RTC
# Consult the PeachCloud GPIO documentation
# (http://docs.peachcloud.org/hardware/gpio_pinout.html) for pinouts

import os
import subprocess
import argparse

from setup_networking import configure_networking
from setup_peach_deb import setup_peach_deb
from update_microservices import update_microservices

# Setup argument parser
parser = argparse.ArgumentParser()
parser.add_argument(
    "user",
    type=str,
    help="username for the default user account")
parser.add_argument("-i", "--i2c", help="configure i2c", action="store_true")
parser.add_argument(
    "-r",
    "--rtc",
    choices=[
        "ds1307",
        "ds3231"],
    help="configure real-time clock")
args = parser.parse_args()

# Ensure RTC configuration requirements are met (if selected)
if args.rtc and not args.i2c:
    parser.error("i2c configuration is required for rtc configuration")

# Save username argument
username = args.user

# Create list of system users for (micro)services
users = [
    "peach-buttons",
    "peach-menu",
    "peach-monitor",
    "peach-network"
    "peach-oled",
    "peach-stats",
    "peach-web"]

# Update Pi and install requirements
print("[ UPDATING OPERATING SYSTEM ]")
subprocess.call(["apt-get", "update", "-y"])
subprocess.call(["apt-get", "upgrade", "-y"])

print("[ INSTALLING SYSTEM REQUIREMENTS ]")
subprocess.call(["apt-get",
                 "install",
                 "vim",
                 "man-db",
                 "locales",
                 "iw",
                 "git",
                 "python-smbus",
                 "i2c-tools",
                 "build-essential",
                 "curl",
                 "libnss-resolve"
                 "mosh",
                 "sudo",
                 "pkg-config",
                 "libssl-dev",
                 "nginx",
                 "wget",
                 "-y"])

# Add the system user with supplied username
print("[ ADDING SYSTEM USER ]")
subprocess.call(["/usr/sbin/adduser", username])
subprocess.call(["usermod", "-aG", "sudo", username])

print("[ CREATING SYSTEM GROUPS ]")
subprocess.call(["/usr/sbin/groupadd", "peach"])
subprocess.call(["/usr/sbin/groupadd", "gpio-user"])

print("[ CREATING SYSTEM USERS ]")
# Peachcloud microservice users
for user in users:
    # Create new system user without home directory and add to `peach` group
    subprocess.call(["/usr/sbin/adduser", "--system",
                     "--no-create-home", "--ingroup", "peach", user])

print("[ ASSIGNING GROUP MEMBERSHIP ]")
subprocess.call(["/usr/sbin/usermod", "-a", "-G",
                 "gpio-user", "peach-buttons"])
subprocess.call(["/usr/sbin/usermod", "-a", "-G", "netdev", "peach-network"])
subprocess.call(["/usr/sbin/usermod", "-a", "-G", "i2c", "peach-oled"])

# Overwrite configuration files
print("[ CONFIGURING OPERATING SYSTEM ]")
print("[ CONFIGURING GPIO ]")
subprocess.call(["cp", "conf/50-gpio.rules",
                 "/etc/udev/rules.d/50-gpio.rules"])

if args.i2c:
    print("[ CONFIGURING I2C ]")
    if not os.path.exists("/boot/firmware/overlays"):
        os.mkdir("/boot/firmware/overlays")
    subprocess.call(["cp", "conf/mygpio.dtbo",
                     "/boot/firmware/overlays/mygpio.dtbo"])
    subprocess.call(["cp", "conf/config.txt_i2c", "/boot/firmware/config.txt"])
    subprocess.call(["cp", "conf/modules", "/etc/modules"])

if args.rtc and args.i2c:
    if args.rtc == "ds1307":
        print("[ CONFIGURING DS1307 RTC MODULE ]")
        subprocess.call(["cp", "conf/config.txt_ds1307",
                         "/boot/firmware/config.txt"])
    elif args.rtc == "ds3231":
        print("[ CONFIGURING DS3231 RTC MODULE ]")
        subprocess.call(["cp", "conf/config.txt_ds3231",
                         "/boot/firmware/config.txt"])
    subprocess.call(["cp", "conf/modules_rtc", "/etc/modules"])
    subprocess.call(["cp", "conf/activate_rtc.sh",
                     "/usr/local/bin/activate_rtc"])
    subprocess.call(["cp", "conf/activate-rtc.service",
                     "/etc/systemd/system/activate-rtc.service"])
    subprocess.call(["systemctl", "daemon-reload"])
    subprocess.call(["systemctl", "enable", "activate-rtc"])

print("[ CONFIGURING NGINX ]")
subprocess.call(
    ["cp", "conf/peach.conf", "/etc/nginx/sites-available/peach.conf"])
subprocess.call(["ln",
                 "-sf",
                 "/etc/nginx/sites-available/peach.conf",
                 "/etc/nginx/sites-enabled/"])

print("[ CONFIGURING LOCALE ]")
subprocess.call(["dpkg-reconfigure", "locales"])

print("[ CONFIGURING CONSOLE LOG-LEVEL PRINTING ]")
subprocess.call(["sysctl", "-w", "kernel.printk=4 4 1 7"])

print("[ CONFIGURING SUDOERS ]")
if not os.path.exists("/etc/sudoers.d"):
    os.mkdir("/etc/sudoers.d")
subprocess.call(["cp", "conf/shutdown", "/etc/sudoers.d/shutdown"])

print("[ CONFIGURING PEACH APT REPO ]")
setup_peach_deb()

print("[ INSTALLING PEACH MICROSERVICES ]")
update_microservices()

# configure networking via setup_networking.py
configure_networking()

print("[ PEACHCLOUD SETUP COMPLETE ]")
print("[ ------------------------- ]")
print("[ please reboot your device ]")


# TODO: flags for installing rust, or just the capabilities to run the services
