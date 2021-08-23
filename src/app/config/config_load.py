import os

import yaml

root_dir = os.path.dirname(os.path.abspath(__file__))
YML_STR_LOAD = "config.yml"

def read_yaml_file():
    '''Load yaml file
    '''
    yml_file = open(os.path.join(root_dir, YML_STR_LOAD))
    doc = yaml.load(yml_file, Loader=yaml.FullLoader)
    return doc

def save_yaml_file(doc):
    '''Save yaml file at once
    '''
    with open(os.path.join(root_dir, YML_STR_LOAD), 'w') as yam:
        yaml.dump(doc, yam)
    return doc
