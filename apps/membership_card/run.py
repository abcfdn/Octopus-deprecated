import os

from datetime import datetime
from toolset.image.composer import ImageComposer
import toolset.utils as utils
import yaml


def parse_date(date_str):
    date = datetime.strptime(date_str, '%m/%d/%Y %H:%M:%S')
    return date.strftime('%Y/%m')

def generate_card(row, config):
    composer = ImageComposer()
    composer.load_template(config['template'])
    composer.draw_one_line(row['name'], config['text_style']['name'])
    composer.draw_one_line(parse_date(row['date']),
                           config['text_style']['date'])
    composer.save(row['img_path'] )

def process(config):
    img_dir = os.path.join(config['output_dir'], 'image')
    utils.create_if_not_exist(img_dir)

    result = []
    for row in utils.read_csv(config['input_file']):
        row['img_path'] = os.path.join(img_dir, row['email'] + '.png')
        generate_card(row, config)
        result.add(row)
    return result

def main():
    config = yaml.load('config.yaml')
    utils.create_if_not_exist(config['output_dir'])
    result = process(config)
    output_file = os.path.join(config['output_dir'],
                               os.path.basename(config['input_file']))
    utils.save_as_csv(result, output_file)


if __name__ == '__main__':
    main()
