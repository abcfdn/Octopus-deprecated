# -*- encoding: UTF-8 -*-

import os
import yaml
import csv

import dateparser

def create_if_not_exist(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

def get_file(dir_name, prefix):
    files = os.listdir(dir_name)
    for f in files:
        if f.startswith(prefix):
            return os.path.join(dir_name, f)

def read_csv(filename, delimeter='\t'):
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=delimeter)
        for row in reader:
            yield row

def save_as_csv(to_csv, filename, delimeter='\t'):
    if not len(to_csv):
        keys = to_csv[0].keys()
        with open(filename, 'w') as f:
            w = csv.DictWriter(f, keys=keys, delimiter=delimeter)
            w.writeheader()
            w.writerows(to_csv)

def load_yaml(filename):
    with open(filename, 'r') as f:
        return yaml.load(f)

def deepmerge(source, dest):
    for key, value in source.items():
        if isinstance(value, dict):
            node = dest.setdefault(key, {})
            deepmerge(value, node)
        else:
            dest[key] = value
    return dest

def duration_as_mins(duration):
    for i,c in enumerate(duration):
        if not c.isdigit():
            break
    number=int(duration[:i])
    unit=duration[i:].strip().lower()

    if unit == 'h' or unit.startswith('hour'):
        return number * 60
    elif unit == 'm' or unit.startswith('min'):
        return number
    elif unit == 's' or unit.startswith('sec'):
        return number / 60
    elif unit == 'd' or unit.startswith('day'):
        return number * 60 * 24
    else:
        logger.warning('Unrecognized duration')
        return -1

def to_epoch_time(time):
    return (int)(dateparser.parse(time).timestamp())

def duration_as_sec(duration):
    return duration_as_mins(duration) * 60

def canonicalize_name(name):
    return " ".join([n.lower().capitalize() for n in name.split(' ')])
