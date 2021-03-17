import subprocess
import argparse
import json
import sys

from peach_config.constants import SERVICES



def run_update_self():
    """
    updates peach-config using apt-get
    :return:
    """
    subprocess.check_call(['apt-get', 'update'])
    subprocess.check_call(['apt-get', 'install', 'python3-peach-config'])


def update_microservices(purge=False):
    """
    installs all peach microservices
    or updates them to the latest version
    except for peach-config
    :param purge: if provided, purges all microservices before re-installing them
    :return: None
    """
    subprocess.check_call(['apt-get', 'update'])

    for service in SERVICES:
        if service == 'python3-peach-config':
            # skip peach-config, which is handled separately
            continue
        if purge:
            print('[ removing {} ]'.format(service))
            subprocess.call(['apt-get', 'remove', service])
            subprocess.call(['apt-get', 'purge', service])
        print('[ installing {} ]'.format(service))
        subprocess.call(['apt-get', 'install', service])


def update(parser):
    # update peach-config (update itself) then run update on all other microservices
    args = parser.parse_args()

    # if -list then just show updates available without running them
    if args.list:
        list_available_updates()
    # just update self
    elif args.self:
        run_update_self()
    # just update other microservices
    elif args.microservices:
        update_microservices(purge=args.purge)
    # update self and then update other microservices
    else:
        run_update_self()
        subprocess.check_call(['/usr/bin/peach-config', 'update', '--microservices'])


def list_available_updates():
    """
    checks if there are any PeachCloud updates available and displays them
    """
    subprocess.check_call(['apt-get', 'update'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    output = subprocess.check_output(["apt", "list", "--upgradable"], stderr=subprocess.DEVNULL).decode(sys.stdout.encoding).strip()
    available_updates = []
    for line in output.splitlines():
        for service in SERVICES:
            if service in line:
                available_updates.append(line)
    print(json.dumps(available_updates))


def init_update_parser(parser):
    # update argument parser
    parser.add_argument("-m", "--microservices", help="update all other peach microservices", action="store_true")
    parser.add_argument("-l", "--list", help="list if there are any updates available without running them", action="store_true")
    parser.add_argument("-s", "--self", help="update peach-config", action="store_true")
    parser.add_argument("-p", "--purge", help="purge old installations when updating", action="store_true")
    return parser


if __name__ == '__main__':
    # Setup argument parser
    parser = argparse.ArgumentParser()
    init_update_parser(parser)
    update(parser)


