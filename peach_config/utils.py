import json
import os


PEACH_DATA_DIR = "/var/lib/peachcloud/"
HARDWARE_CONFIG_FILE = os.path.join(PEACH_DATA_DIR, "hardware_config.json")


def save_hardware_config(i2c, rtc):
    """
    helper function to store what hardware configuration a particular peach was setup with
    """
    hardware_config = {
        "i2c": i2c,
        "rtc": rtc
    }
    if not os.path.exists(PEACH_DATA_DIR):
        os.makedirs(PEACH_DATA_DIR)
    with open(HARDWARE_CONFIG_FILE, 'w') as f:
        f.write(json.dumps(hardware_config))


def load_hardware_config():
    """
    helper function to load the hardware configuration used last time setup_peach.py successfully ran
    """
    if os.path.exists(HARDWARE_CONFIG_FILE):
        with open(HARDWARE_CONFIG_FILE, 'r') as f:
            hardware_config = json.loads(f.read())
        return hardware_config
    else:
        return None