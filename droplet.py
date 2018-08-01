import os
import digitalocean
from typing import List
token = os.environ["DIGITAL_OCEAN_API_TOKEN"]
manager = digitalocean.Manager(token=token)


def main():
    my_droplets: List = manager.get_all_droplets()
    if len(my_droplets) == 0:
        create_droplet()


def create_droplet():
    from digitalocean import SSHKey
    user_ssh_key = open('/Users/mralph/.ssh/bbk_id_rsa.pub').read()
    key = SSHKey(token=token,
                 name='bbk_id_rsa_pub',
                 public_key=user_ssh_key)

    key.create()

    keys = manager.get_all_sshkeys()

    droplet = digitalocean.Droplet(token=os.environ["DIGITAL_OCEAN_API_TOKEN"],
                                   name='matt-masters-project',
                                   region='lon1',
                                   image='ubuntu-18-04-x64',
                                   size_slug='s-1vcpu-1gb',
                                   ssh_keys=keys,
                                   backups=False)

    droplet.create()

    actions = droplet.get_actions()
    for action in actions:
        action.load()
        print(action.status)


if __name__ == "__main__":
    main()
