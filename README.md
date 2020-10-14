# peach-config

Configuration instructions, files and scripts for deploying PeachCloud. 

_Work in progress._

**Network**

In this configuration, the RPi connects to other networks with the `wlan0` interface and deploys an access point on the `ap0` interface. Only one of these modes is active at a time (client or access point).

Networking is handled with `wpa_supplicant`, `hostapd` and `dnsmasq`.

### Prerequisite Steps

Download the latest Debian Buster preview image for RPi3 and flash it to an SD card (card is located at `/dev/mmcblk0` in this case):

`wget https://people.debian.org/~gwolf/raspberrypi3/20190628/20190628_raspberry-pi-3_buster_PREVIEW.img.xz`  
`xzcat 20190628_raspberry-pi-3_buster_PREVIEW.img.xz | sudo dd of=/dev/mmcblk0 bs=64k oflag=dsync status=progress`

### Setup

Quick setup commands to connect to a local WiFi network over the `wlan0` interface (assuming `eth0` connection is not possible):

```bash
# username
root
# password
raspberry
# set interface up
ip link set wlan0 up
# append ssid and password for wifi access point
wpa_passphrase <SSID> <PASS> > /etc/wpa_supplicant/wpa_supplicant.conf
# open wpa_supplicant.conf
nano /etc/wpa_supplicant/wpa_supplicant.conf
```

[ Add the following two lines to top of file ]

```bash
ctrl_interface=/run/wpa_supplicant
update_config=1
```

[ Save and exit ]

```bash
# open network interfaces config
nano /etc/network/interfaces
```

[ Add the following lines to the file ]

```
auto lo
iface lo inet loopback

allow-hotplug wlan0
auto wlan0
iface wlan0 inet dhcp
    wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf
```

[ Save and exit ]

`reboot now`

[ Pi should now be connected to the WiFi network ]

### Scripts

Includes `activate_ap.sh` and `activate_client.sh`. These two scripts allow easy switching between client and access point modes.

The `setup_dev_env.py` script can be executed once your Pi is internet-connected and `git` and `python` have been installed. It takes a `<USER>` argument to create a new system user. You will be prompted to enter a password for your newly created user. The script will install system requirements and copy configuration files relating to networking, I2C and RTC.

_TODO: Add flags to (de)select I2C, RTC and Rust install & config. Flags should also be added which allow the installer to choose between development environment and release environment configuration._

`apt update`  
`apt install git python`  
`git clone https://github.com/peachcloud/peach-config.git`  
`cd peach-config`  
`python scripts/setup_dev_env.py <USER>`


**IMPORTANT: Please do not forget to set a new password for the root user!**

### Licensing

AGPL-3.0
