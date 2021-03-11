import subprocess
import sys
import re
import json


def get_currently_installed_microservices():
    packages = subprocess.check_output(["apt", "list", "--installed"]).decode(sys.stdout.encoding).strip()
    peach_packages = re.finditer(r'(\S+)/buster,now (\S+) \S+.*\n', packages)
    package_dict = {}
    for package in peach_packages:
        package_dict[package.group(1)] = package.group(2)

    # return dictionary mapping package name to version
    return package_dict


def get_last_installed_hardware_configuration():
    return {
        "i2c": True,
        "rtc": "ds123"
    }


def generate_manifest():
    packages = get_currently_installed_microservices()
    configuration = get_last_installed_hardware_configuration()
    manifest = {
        "packages": packages,
        "hardware": configuration
    }
    print(json.dumps(manifest))


if __name__ == '__main__':
    generate_manifest()