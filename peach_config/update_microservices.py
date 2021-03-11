import subprocess
import argparse


def update_microservices(purge=False):
    """
    installs all peach microservices
    or updates them to the latest version
    :param purge: if provided, purges all microservices before re-installing them
    :return: None
    """
    subprocess.call(['apt-get', 'update'])

    SERVICES = [
        "peach-oled",
        "peach-network",
        "peach-stats",
        "peach-web",
        "peach-menu",
        "peach-buttons",
        "peach-monitor",
        "peach-probe",
        "peach-go-sbot",
    ]

    for service in SERVICES:
        if purge:
            print('[ removing {} ]'.format(service))
            subprocess.call(['apt-get', 'remove', service])
            subprocess.call(['apt-get', 'purge', service])
        print('[ installing {} ]'.format(service))
        subprocess.call(['apt-get', 'install', service])


if __name__ == '__main__':
    # Setup argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--purge", help="update microservices and purge old installations", action="store_true")
    args = parser.parse_args()

    update_microservices(purge=args.purge)
