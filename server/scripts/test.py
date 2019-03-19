# -*- encoding: UTF-8 -*-

import os
import sys
sys.path.append("..")

import datetime

from server.db.service import Service
import server.platforms.utils.util as util
from server.platforms.google.photo import GooglePhoto

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT_DIR, 'config.yaml')
COMMON_CONFIG_PATH = os.path.join(ROOT_DIR, '../config.yaml')

MCARD_ALBUM_ID = "AGQRtP839EFOmh7vZZCSzPOfeU53lj6_Niytt5KyKJmj6Lh2vKGON-70RGjuQ5m77fnSDl9kDQsOrcj0LJNad4Wj6YbMfteGTg"
POST_ALBUM_ID = "AGQRtP8Uj40efSoim2TAUe7j9uETcEpG3qoaUMJlP2-_wbZxBtqUpuTHJ7vQvYIFqjmxvufSIq45pjORmnU989in1qkga71iWQ"


def test_mongo():
    config = util.load_yaml(CONFIG_PATH)
    common_config = util.load_yaml(COMMON_CONFIG_PATH)
    config.update(common_config)
    service = Service(config['mongo'])
    print(service.get_recent_sessions())


def test_photo():
    config = util.load_yaml(COMMON_CONFIG_PATH)
    service = GooglePhoto(config['google'])
    filepath = "/tmp/abc_apps/whitepaper_journal/event_poster/output/blockspace_20190215.jpg"
    service.create_item(POST_ALBUM_ID, filepath, "poster for test")

def main():
    test_photo()

if __name__ == '__main__':
    main()
