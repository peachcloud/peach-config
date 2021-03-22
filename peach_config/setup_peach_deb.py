# setup_peach_deb.py
# Standalone script to configure a Debian installation to add the peach apt repository
# and install all peach microservices to the latest version

import subprocess
import os

from peach_config.constants import PROJECT_PATH
from peach_config.update import update_microservices



def setup_peach_deb():
    """
    Adds apt.peachcloud.org to the list of debian apt sources and sets the public key appropriately
    """
    subprocess.call(["cp", os.path.join(PROJECT_PATH, "conf/peach.list"), "/etc/apt/sources.list.d/peach.list"])
    # add public key
    subprocess.call(["wget", "-O", "/tmp/pubkey.gpg", "http://apt.peachcloud.org/pubkey.gpg"])
    subprocess.call(["apt-key", "add", "/tmp/pubkey.gpg"])
    subprocess.call(["rm", "/tmp/pubkey.gpg"])


if __name__ == '__main__':
    setup_peach_deb()
    update_microservices()
