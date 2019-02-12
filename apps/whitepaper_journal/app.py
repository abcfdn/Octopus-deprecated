# -*- encoding: UTF-8 -*-

import os

from toolset.google.sheet import GoogleSheet
from app.base import App

FORMAT = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('whitepaper_journal_app')


class WhitepaperJournal(App):
    def __init__(self):
        super().__init__()

    def create_poster(self, events, topics):
        drive_service = GoogleDrive(self.config['GOOGLE'])
        poster = WhitepaperJournalPoster(drive_service, self.config['POSTER'])
        for topic in topics:
            filtered = [event for event in events if event['topic'] == topic]
            poster.add_topic(filtered)
        poster.compose()

    def run(self):
        sheet_service = GoogleSheet(self.config['GOOGLE'])
        events = sheet_service.read_as_map(self.config['INPUT']['event'], 2, 10)
        events = sorted(events, key=lambda k: k['date'])
        self.create_poster(events, ['Generalized Mining', 'Consensus'])


def main():
    app = WhitepaperJournal()
    app.run()


if __name__ == '__main__':
    main()
