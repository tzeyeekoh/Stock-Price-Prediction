import os

import yaml

root_dir = os.path.dirname(os.path.abspath(__file__))
yml_name = "config.yml"

def read_config():
    '''Load yaml file
    '''
    yml_file = open(os.path.join(root_dir, yml_name))
    doc = yaml.load(yml_file, Loader=yaml.FullLoader)
    return doc

def save_config(doc):
    '''Save yaml file at once
    '''
    with open(os.path.join(root_dir, yml_name), 'w') as yam:
        yaml.dump(doc, yam)
    return doc
