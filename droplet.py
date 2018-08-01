import os
import digitalocean
from digitalocean import SSHKey
from typing import List
token = os.environ["DIGITAL_OCEAN_API_TOKEN"]
manager = digitalocean.Manager(token=token)


def main():
    my_keys: List = manager.get_all_sshkeys()
    if len(my_keys) == 0:
        create_key()
    my_droplets: List = manager.get_all_droplets()
    if len(my_droplets) == 0:
        create_droplet()


def create_key():
    user_ssh_key = open('/Users/mralph/.ssh/bbk_id_rsa.pub').read()
    key = SSHKey(token=token,
                 name='bbk_id_rsa_pub',
                 public_key=user_ssh_key)

    key.create()


def create_droplet():
    keys = manager.get_all_sshkeys()

    droplet = digitalocean.Droplet(token=os.environ["DIGITAL_OCEAN_API_TOKEN"],
                                   name='matt-masters-project',
                                   region='lon1',
                                   image='ubuntu-18-04-x64',
                                   size_slug='s-1vcpu-2gb',
                                   ssh_keys=keys,
                                   backups=False)

    droplet.create()

    actions = droplet.get_actions()
    for action in actions:
        action.load()
        print(action.status)

    get_ip_address()


def get_ip_address():
    droplets = manager.get_all_droplets()
    droplet = droplets[0]
    print(droplet.ip_address)


if __name__ == "__main__":
    main()
