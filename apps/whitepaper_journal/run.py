# -*- encoding: UTF-8 -*-

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import copy
from toolset.image.composer import ImageComposer, ImagePiece
from toolset.google.sheet import GoogleSheet
import toolset.utils as utils
from app import App


class WhitepaperJournalPoster:
    def __init__(self, settings):
        self.settings = settings
        self.init_imgs()

    def init_imgs(self):
        template_path = self.settings['template_path']
        self.header = ImagePiece(os.path.join(template_path, 'header.png'))
        self.tail = ImagePiece(os.path.join(template_path, 'tail.png'))
        self.schedule = ImagePiece(os.path.join(template_path, 'schedule.png'))
        self.event_sep = ImagePiece(os.path.join(template_path, 'item_sep.png'))
        self.logo = ImagePiece(os.path.join(template_path, 'logo.png'))
        self.content = [self.header, self.schedule]

    # events should belong to same topic
    def add_topic(self, events):
        if not len(events):
            return

        topic = events[0]['topic']
        topic_img = ImagePiece(os.path.join(self.settings['template_path'],
                                            'topic.png'))
        topic_img.draw_text('Topic: ' + topic,
                            self.settings['text_style']['topic'])
        self.content.append(topic_img)

        event_imgs =[self.create_event(event) for event in events]
        event_seps = [self.event_sep] * len(event_imgs)
        self.content.extend([img for pair in zip(event_imgs, event_seps)
                                  for img in pair][:-1])

    def create_event(self, event):
        event_img = ImagePiece(os.path.join(self.settings['template_path'],
                                            'item.png'))
        event_img.draw_text('{} {}'.format(event['date'], event['time']),
                            self.settings['text_style']['date'])
        event_img.draw_text(event['session_name'],
                            self.settings['text_style']['session_name'])
        event_img.draw_text(event['presenter_name'],
                            self.settings['text_style']['presenter_name'])
        event_img.draw_text(event['presenter_title'],
                            self.settings['text_style']['presenter_title'])
        event_img.draw_text(event['address1'] + '\n' + event['address2'],
                            self.settings['text_style']['address'])
        return event_img

    def compose(self):
        self.content.append(self.tail)
        composer = ImageComposer(self.content)
        composer.vertical_combine()
        return composer.save('./new_post.png')


class WhitepaperJournal(App):
    def __init__(self):
        super().__init__()

    def load_events(self):
        service = GoogleSheet(self.config['GOOGLE'])
        return service.read_as_map(
            self.config['GOOGLE']['SHEET_ID'], 2, 10)

    def create_poster(self, events, topics):
        poster = WhitepaperJournalPoster(self.config['POSTER'])
        for topic in topics:
            filtered = [event for event in events if event['topic'] == topic]
            poster.add_topic(filtered)
        poster.compose()

    def run(self):
        events = sorted(self.load_events(), key=lambda k: k['date'])
        self.create_poster(events, ['Generalized Mining', 'Consensus'])


def main():
    app = WhitepaperJournal()
    app.run()


if __name__ == '__main__':
    main()
