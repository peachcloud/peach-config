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
        {"name": "peach-oled", "repo_url": "https://github.com/peachcloud/peach-oled.git"},
        {"name": "peach-network", "repo_url": "https://github.com/peachcloud/peach-network.git"},
        {"name": "peach-stats", "repo_url": "https://github.com/peachcloud/peach-stats.git"},
        {"name": "peach-web", "repo_url": "https://github.com/peachcloud/peach-web.git"},
        {"name": "peach-menu", "repo_url": "https://github.com/peachcloud/peach-menu.git"},
        {"name": "peach-buttons", "repo_url": "https://github.com/peachcloud/peach-buttons.git"},
        {"name": "peach-monitor", "repo_url": "https://github.com/peachcloud/peach-monitor.git"}
    ]

    for service in SERVICES:
        name = service['name']
        if purge:
            print('[ removing {} ]'.format(name))
            subprocess.call(['apt-get', 'remove', name])
            subprocess.call(['apt-get', 'purge', name])
        print('[ installing {} ]'.format(name))
        subprocess.call(['apt-get', 'install', name])



if __name__ == '__main__':

    # Setup argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--purge", help="update microservices and purge old installations", action="store_true")
    args = parser.parse_args()

    update_microservices(purge=args.purge)
