# -*- encoding: UTF-8 -*-

import os
import sys
sys.path.append("..")

from server.db.service import Service
import server.platforms.utils.util as util

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT_DIR, 'config.yaml')
COMMON_CONFIG_PATH = os.path.join(ROOT_DIR, '../config.yaml')


def main():
    config = util.load_yaml(CONFIG_PATH)
    common_config = util.load_yaml(COMMON_CONFIG_PATH)
    config.update(common_config)
    service = Service(config['mongo'])
    print(service.get_recent_sessions())


if __name__ == '__main__':
    main()
