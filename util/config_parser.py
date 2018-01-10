import yaml


def parse_config():
    with open('./config.yml') as config:
        conf = yaml.load(config)
        return conf
