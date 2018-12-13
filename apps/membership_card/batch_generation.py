import csv
import os
import base64
from datetime import datetime
import yaml
from toolset.image.composer import ImageComposer
import toolset.utils as utils
from web3.auto import w3

CONFIG_FILE = 'config.yaml'

def load_config():
    return yaml.load(CONFIG_FILE)

def parse_input(filename):
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        next(reader, None)  # skip the header
        for row in reader:
            yield row

def parse_date(date_str):
    date = datetime.strptime(date_str, '%m/%d/%Y %H:%M:%S')
    return date.strftime('%Y/%m')


config = load_config()

utils.create_if_not_exist(config['output_dir'])
output_file = os.path.join(config['output_dir'], 'members.csv')

composer = ImageComposer()
for [since, email, name] in utils.read_csv(INPUT):
    composer.load_template(config['template'])
    composer.draw_one_line(name, config['text_style']['name'])
    composer.draw_one_line(parse_date(date_str),
                           config['text_style']['date'])
    composer.save('./output/images/' + email + '.png')
