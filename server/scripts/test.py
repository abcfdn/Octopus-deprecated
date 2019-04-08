# -*- encoding: UTF-8 -*-

import os
import sys
sys.path.append("..")

import logging
import csv
import json
import datetime

from server.db.service import Service
import server.platforms.utils.util as util
from server.platforms.google.photo import GooglePhoto
from server.platforms.imgur import Imgur
from server.workflow.tasks.whitepaper_journal.event_poster import WhitepaperJournalEventPoster
from server.scripts.data_sync import DataSync
from server.workflow.tasks.membership.sync import MemberSync
from server.db.mongo import MongoConnection, MemberStore
from google.oauth2 import service_account

from pprint import pprint

FORMAT = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('script')
logger.setLevel(logging.INFO)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT_DIR, 'config.yaml')
COMMON_CONFIG_PATH = os.path.join(ROOT_DIR, '../config.yaml')

MCARD_ALBUM_ID = "AGQRtP839EFOmh7vZZCSzPOfeU53lj6_Niytt5KyKJmj6Lh2vKGON-70RGjuQ5m77fnSDl9kDQsOrcj0LJNad4Wj6YbMfteGTg"
POST_ALBUM_ID = "AGQRtP8Uj40efSoim2TAUe7j9uETcEpG3qoaUMJlP2-_wbZxBtqUpuTHJ7vQvYIFqjmxvufSIq45pjORmnU989in1qkga71iWQ"


def config():
    config = util.load_yaml(CONFIG_PATH)
    common_config = util.load_yaml(COMMON_CONFIG_PATH)
    config.update(common_config)
    return config


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


def google_creds(config):
    creds_file = config['google']['service_account']
    scopes = config['google']['scopes']
    creds = service_account.Credentials.from_service_account_file(
        creds_file, scopes=scopes)
    return creds.with_subject('contact@abcer.world')


def event_poster():
    config = util.load_yaml(COMMON_CONFIG_PATH)
    WhitepaperJournalEventPoster(google_creds(config)).process(1550875924)


def data_sync():
    DataSync(config()).sync()

def member_sync():
    config = util.load_yaml(COMMON_CONFIG_PATH)
    MemberSync(google_creds(config), config['imgur'], config['mongo']).sync_membership_card()

def member_card_test():
    config = util.load_yaml(COMMON_CONFIG_PATH)
    imgur = Imgur(config['imgur']['creds_file'])
    photos = imgur.get_photos('TTA1Bp4')
    imgur.upload_photos(photos, 'XaBxokL')
    pprint(photos[0].__dict__)

def get_member_info():
    config = util.load_yaml(COMMON_CONFIG_PATH)
    conn = MongoConnection(config['mongo'])
    store = MemberStore(conn)
    members = store.find_all({}, max_cnt=1000)
    with open('/root/members.csv', 'w') as f:
        fieldnames = ['name', 'email', 'card']
        writer = csv.DictWriter(f, delimiter=',', fieldnames=fieldnames)
        writer.writeheader()
        for member in members:
            row = {
                'name': member.get('name', ''),
                'email': member.get('email', ''),
                'card': member.get('membership_card', {}).get('baseUrl', '')
            }
            writer.writerow(row)


def main():
    member_card_test()

if __name__ == '__main__':
    main()
