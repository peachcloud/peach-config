import os
import subprocess


username = 'peach'


def update_microservices():
    print("[ UPDATING MICROSERVICES ]")
    microservices_dir = '/home/{}/microservices'.format(username)
    if not os.path.exists(microservices_dir): os.makedirs(microservices_dir)
    microservices = [
        'peach-oled',
        'peach-menu',
        'peach-network',
        'peach-stats',
        'peach-buttons',
        'peach-monitor',
        'peach-oled'
    ]
    VPS_URL = 'http://167.99.136.83'
    for service in microservices:
        print("[ UPDATING MICROSERVICE {} ]".format(service))
        service_url = '{}/{}'.format(VPS_URL, service)
        download_path = os.path.join(microservices_dir, service)
        # TODO: to save time, we could do some type of check  which checks the version of the downloaded file
        # and the version of the latest release, and only deletes & updates if the version is newer
        if os.path.exists(download_path): os.remove(download_path)
        subprocess.call(['wget', service_url, '-O', download_path])


if __name__ == '__main__':
    update_microservices()