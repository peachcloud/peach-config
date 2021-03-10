## Installation From PeachCloud Disc Image

#### Step 1: Flash The SD Card

Download the latest PeachCloud image from http://releases.peachcloud.org and flash it to an SD card.

_Note:_ Be sure to use the correct device location in the `dd` command, otherwise you risk wiping another connected USB device. `sudo dmesg | tail` can be run after plugging in the SD card to determine the correct device location:

```bash
wget https://raspi.debian.net/verified/20200831_raspi_3.img.xz
xzcat 20200831_raspi_3.img.xz | sudo dd of=/dev/sdb bs=64k oflag=dsync status=progress
```

On Mac OS, use the following command to flash the SD card:

`xzcat 20200831_raspi_3.img.xz | sudo dd of=/dev/sdcarddisc`

Alternatively, use [Etcher](https://www.balena.io/etcher/).

_Note:_ If the above image link stops working, you can find the complete list of Raspberry Pi Debian images [here](https://raspi.debian.net/tested-images/).

Your SD card now has a complete PeachCloud installation on it and is ready to use. 


#### Step 2: Connecting To The Internet 

## Via peach.local

TODO: write this documentation

## Via a Screen

TODO: write this documentation


#### Step 3: Getting Started

TODO: write this documentation