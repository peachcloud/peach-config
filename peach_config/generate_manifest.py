import subprocess
import sys
import re
import json

from peach_config.utils import load_hardware_config


def get_currently_installed_microservices():
    packages = subprocess.check_output(["dpkg", "-l"]).decode(sys.stdout.encoding).strip()
    peach_packages = re.finditer(r'\S+\s+(\S*peach\S+)\s+(\S+).*\n', packages)
    package_dict = {}
    for package in peach_packages:
        package_dict[package.group(1)] = package.group(2)

    # return dictionary mapping package name to version
    return package_dict


def generate_manifest():
    packages = get_currently_installed_microservices()
    hardware_config = load_hardware_config()
    if not hardware_config:
        hardware_config = "No PeachCloud hardware config found"
    manifest = {
        "packages": packages,
        "hardware": hardware_config,
    }
    print(json.dumps(manifest))


if __name__ == '__main__':
    generate_manifest()