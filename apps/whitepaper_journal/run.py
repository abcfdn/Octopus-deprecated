# -*- encoding: UTF-8 -*-

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toolset.image.composer import ImageComposer, ImagePiece
from toolset.google.sheet import GoogleSheet
import toolset.utils as utils

from app import App


class WhitepaperJournalPoster:
    def __init__(self, tempalte_path):
        self.header = ImagePiece(os.path.join(tempalte_path, 'header.png'))
        self.schedule = ImagePiece(os.path.join(tempalte_path, 'schedule.png'))
        self.topic = ImagePiece(os.path.join(tempalte_path, 'topic.png'))
        self.item = ImagePiece(os.path.join(tempalte_path, 'item.png'))
        self.item_sep = ImagePiece(os.path.join(tempalte_path, 'item_sep.png'))
        self.logo = ImagePiece(os.path.join(tempalte_path, 'logo.png'))

    def compose(self):
        self.composer = self.ImageComposer([self.header,
                                            self.schedule,
                                            self.topic,
                                            self.item,
                                            self.item_sep])


class WhitepaperJournal(App):
    def __init__(self):
        super().__init__()

    def load_input(self):
        service = GoogleSheet(self.config['GOOGLE'])
        return service.read_as_map(
            self.config['GOOGLE']['SHEET_ID'], 2, 10)

    def create_poster_by_topics(self, events, topics):
        filtered = [event for event in events if event['topic'] in topics]


    def run(self):
        events = sorted(self.load_input(), key=lambda k: k['date'])
        self.create_poster_by_topics(
            events, ['Generalized Mining', 'Consensus'])


def main():
    app = WhitepaperJournal()
    app.run()


if __name__ == '__main__':
    main()
