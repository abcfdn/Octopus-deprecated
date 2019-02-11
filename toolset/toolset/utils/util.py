# -*- encoding: UTF-8 -*-

import os
import csv

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
