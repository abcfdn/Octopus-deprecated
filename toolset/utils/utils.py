# -*- encoding: UTF-8 -*-

import os
import csv
from web3.auto import w3

def create_if_not_exist(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

def eth_account_from_email(email):
    seed = (email * (int(32/len(email))+1))[:32]
    acct = w3.eth.account.create(seed.upper())
    return acct.address, acct.privateKey.hex()

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