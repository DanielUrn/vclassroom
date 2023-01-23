import os
import yaml

script_path = os.path.dirname(__file__)
config_file_name = "config.yml"
config_file = os.path.join(script_path, config_file_name)

with open(config_file, 'r') as stream:
    try:
        config = yaml.safe_load(stream)['config']
    except yaml.YAMLError as exc:
        print(exc)

def read_config(property):
    return config.get(property)


