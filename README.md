# peach-config

![Generic badge](https://img.shields.io/badge/version-0.2.4-<COLOR>.svg)

Configuration instructions, files and scripts for deploying PeachCloud. 

_Work in progress._

## Prerequisite Steps

Download the latest Debian Buster preview image for RPi3 and flash it to an SD card.

_Note:_ Be sure to use the correct device location in the `dd` command, otherwise you risk wiping another connected USB device. `sudo dmesg | tail` can be run after plugging in the SD card to determine the correct device location:

```bash
wget https://raspi.debian.net/verified/20200831_raspi_3.img.xz
xzcat 20200831_raspi_3.img.xz | sudo dd of=/dev/sdb bs=64k oflag=dsync status=progress
```

On Mac OS, use the following command to flash the SD card:

`xzcat 20200831_raspi_3.img.xz | sudo dd of=/dev/sdcarddisc`

Alternatively, use [Etcher](https://www.balena.io/etcher/).

_Note:_ If the above image link stops working, you can find the complete list of Raspberry Pi Debian images [here](https://raspi.debian.net/tested-images/).

## Setup

Quick setup commands to connect to a local WiFi network over the `wlan0` interface (assuming `eth0` connection is not possible):

```bash
# username
root
# password (by default raspberry debian requires no password, so we set the password for root here)
passwd
# set interface up (run command twice if you receive 'link is not ready' error on first try)
ip link set wlan0 up
# append ssid and password for wifi access point
wpa_passphrase <SSID> <PASS> > /etc/wpa_supplicant/wpa_supplicant.conf
# open wpa_supplicant.conf
nano /etc/wpa_supplicant/wpa_supplicant.conf
```

[ Add the following two lines to top of file ]

```plaintext
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
```

[ Save and exit ]

```bash
# open network interfaces config
nano /etc/network/interfaces
```

[ Add the following lines to the file ]

```plaintext
auto lo
iface lo inet loopback

auto eth0
allow-hotplug eth0
iface eth0 inet dhcp

auto wlan0
allow-hotplug wlan0
iface wlan0 inet dhcp
    wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf
```


[ Save and exit ]

`reboot now`

[ Pi should now be connected to the WiFi network ]

## Scripts

**System Configuration**

The `setup_dev_env.py` script can be executed once your Pi is internet-connected and `git` and `python` have been installed. 

```bash
# commands assume the use of the `root` user (otherwise first run `sudo -Es`)
apt update
apt install git python
git clone https://github.com/peachcloud/peach-config.git
cd peach-config
# run the script with --i2c and --rtc flags to configure
python scripts/setup_dev_env.py -i -r ds3231 <USER>
```

Running the script with the `-h` flag shows the help menu:

```bash
usage: setup_dev_env.py [-h] [-i] [-r {ds1307,ds3231}] user

positional arguments:
  user                  username for the default user account
  
optional arguments:
  -h, --help            show this help message and exit
  -i, --i2c             configure i2c
  -r {ds1307,ds3231}, --rtc {ds1307,ds3231}
                        configure real-time clock
```

A `<USER>` argument must be supplied to create a new system user. You will be prompted to enter a password for your newly created user.

The script also allows optional configuration of I2C and real-time clock (RTC) modules. I2C configuration is necessary for the OLED display and physical interface to work correctly. RTC configuration is required for the real-time clock to work correctly. When passing the `-r` flag, the type of real-time clock module must be included (either ds1307 or ds3231). Selecting real-time clock configuration will not work if the I2C flag is not selected (in other words, the real-time clock requires I2C).

Run the script as follows for a full installation and configuration with I2C and the ds3231 RTC module (username in this case is `peach`):

`python scripts/setup_dev_env.py -i -r ds3231 peach`

**Network**

Networking is handled by `wpa_supplicant` and `systemd-networkd`.

The RPi connects to other networks with the `wlan0` interface and deploys an access point on the `ap0` interface. Only one of these modes is active at a time (client or access point). The RPi boots in client mode by default.

To switch to access point mode:

`sudo systemctl start wpa_supplicant@ap0.service`

To switch to client mode:

`sudo systemctl start wpa_supplicant@wlan0.service`

_Note:_ No stopping of services or rebooting is required.

To enable access point mode on boot:

```bash
sudo systemctl disable wpa_supplicant@wlan0.service
sudo systemctl enable wpa_supplicant@ap0.service
```

A standalone networking configuration script is included in this repository (`scripts/setup_networking.py`). Network-related documentation can also be found in this repository (`docs`).

## Connecting

Once the setup script has been run, connect to the system remotely over the local network using ssh or mosh:

`ssh user@peach.local` or `mosh user@peach.local`

There is a file with detailed instructions on how to connect via a direct ethernet cable located in `docs/direct-ethernet-setup.md`

## Troubleshooting

You may encounter DNS issues if your system time is inaccurate. Please refer to this [StackExchange answer](https://unix.stackexchange.com/a/570382/450882) for details. The steps to remedy the situation are offered here in brief:

```bash
sudo -Es
timedatectl set-ntp 0
# edit this line according to your current date & time
timedatectl set-time "2021-01-13 11:37:10"
timedatectl set-ntp 1
exit
```

## Licensing

AGPL-3.0
