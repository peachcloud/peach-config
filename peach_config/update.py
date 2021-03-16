import subprocess
import argparse



def run_update_self():
    """
    updates peach-config using apt-get
    :return:
    """
    subprocess.check_call(['apt-get', 'update'])
    subprocess.check_call(['apt-get', 'install', 'python3-peach-config'])


def update_others(purge=False):
    """
    installs all peach others
    or updates them to the latest version
    :param purge: if provided, purges all others before re-installing them
    :return: None
    """
    subprocess.check_call(['apt-get', 'update'])

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


def update(parser):
    # update peach-config (update itself) then run update on all other others
    args = parser.parse_args()

    # just update self
    if args.self:
        run_update_self()
    # just update other others
    elif args.others:
        update_others(purge=args.purge)
    # update self and then update other others
    else:
        run_update_self()
        subprocess.check_call(['/usr/bin/peach-config', 'update', '--others'])


def init_update_parser(parser):
    # update argument parser
    parser.add_argument("-m", "--others", help="update all other peach microservices", action="store_true")
    parser.add_argument("-s", "--self", help="update peach-config", action="store_true")
    parser.add_argument("-p", "--purge", help="purge old installations when updating", action="store_true")
    return parser


if __name__ == '__main__':
    # Setup argument parser
    parser = argparse.ArgumentParser()
    init_update_parser(parser)
    update(parser)


