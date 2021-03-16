# peach-config

![Generic badge](https://img.shields.io/badge/version-0.2.10-<COLOR>.svg)

Python module which handles installation and updating for PeachCloud.

## Installation From PeachCloud Disc Image

The recommended way to install PeachCloud is to download the latest PeachCloud disc image from http://releases.peachcloud.org, 
and flash it to an SD card. peach-config is included as part of this disc image, and can then 
be used as a tool for updating PeachCloud as needed. 

You can find detailed instructions on setting up PeachCloud from a PeachCloud disc image [here](docs/installation-from-peach-disc-image.md). 

## Installation From Debian Disc Image

You can find a guide for installing plain Debian onto a Raspberry pi [here](docs/installation-from-debian-disc-image.md).

Once you have Debian running on your pi, you can install peach-config by adding the PeachCloud apt repository and using apt. 

To add the PeachCloud Debian package archive as an apt source, run the following commands from your Pi:

``` bash
echo "deb http://apt.peachcloud.org/ buster main" > /etc/apt/sources.list.d/peach.list
wget -O - http://apt.peachcloud.org/pubkey.gpg | sudo apt-key add -
```

You can then install peach-config with apt:

``` bash
sudo apt-get update
sudo apt-get install python3-peach-config
```

peach-config has only been tested on a Raspberry Pi 3 B+ running Debian 10. 


## Usage

The peach-config debian module installs a command-line tool to `/usr/bin/peach-config`.

`peach-config` is a tool for installing PeachCloud and for updating it. 

`peach-config -h` shows the help menu:

```bash
usage: peach-config [-h] [-i] [-n] [-d] [-r {ds1307,ds3231}] user

positional arguments:
  user                  username for the default user account

optional arguments:
  -h, --help            show this help message and exit
  -i, --i2c             configure i2c
  -n, --noinput         run setup without user input
  -d, --defaultlocale   set default locale to en_US.UTF-8 for compatability
  -r {ds1307,ds3231}, --rtc {ds1307,ds3231}
                        configure real-time clock
```

A `<USER>` argument must be supplied to create a new system user. You will be prompted to enter a password for your newly created user.

The script also allows optional configuration of I2C and real-time clock (RTC) modules. I2C configuration is necessary for the OLED display and physical interface to work correctly. RTC configuration is required for the real-time clock to work correctly. When passing the `-r` flag, the type of real-time clock module must be included (either ds1307 or ds3231). Selecting real-time clock configuration will not work if the I2C flag is not selected (in other words, the real-time clock requires I2C).

Run the script as follows for a full installation and configuration with I2C and the ds3231 RTC module (username in this case is `peach`):

`peach-config -i -r ds3231 peach`


## Licensing

AGPL-3.0
