# -*- encoding: UTF-8 -*-

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import copy
from toolset.image.composer import ImageComposer, ImagePiece
from toolset.google.sheet import GoogleSheet
from toolset.google.drive import GoogleDrive
import toolset.utils.util as util
from app import App


class WhitepaperJournalPoster:
    TXT_FIELDS = ['datetime', 'session_name', 'presenter_name',
                  'presenter_title', 'address']
    IMG_FIELDS = ['presenter_avatar']

    def __init__(self, drive_service, settings):
        self.drive_service = drive_service
        self.text_style = settings['txt_style']
        self.img_style = settings['img_style']

        self.init_cache(settings['cache'])
        self.init_imgs()

    def init_cache(self, cache_settings):
        local_path = cache_settings['local_path']
        util.create_if_not_exist(local_path)

        self.template_path = os.path.join(local_path, 'template')
        util.create_if_not_exist(self.template_path)
        self.drive_service.sync_folder(cache_settings['template'], self.template_path)

        self.avatars_path = os.path.join(local_path, 'avatars')
        util.create_if_not_exist(self.avatars_path)
        self.drive_service.sync_folder(cache_settings['avatars'], self.avatars_path)

    def init_imgs(self):
        header_file = os.path.join(self.template_path, 'header.png')
        self.header = ImagePiece.from_file(header_file)

        tail_file = os.path.join(self.template_path, 'tail.png')
        self.tail = ImagePiece.from_file(tail_file)

        schedule_file = os.path.join(self.template_path, 'schedule.png')
        self.schedule = ImagePiece.from_file(schedule_file)

        event_sep_file = os.path.join(self.template_path, 'item_sep.png')
        self.event_sep = ImagePiece.from_file(event_sep_file)

        logo_file = os.path.join(self.template_path, 'logo.png')
        self.logo = ImagePiece(logo_file)

        self.content = [self.header, self.schedule]

    # events should belong to same topic
    def add_topic(self, events):
        if not len(events):
            return

        topic_file = os.path.join(self.template_path, 'topic.png')
        topic_img = ImagePiece.from_file(topic_file)
        topic = events[0]['topic']
        topic_img.draw_text('Topic: ' + topic, self.text_style['topic'])
        self.content.append(topic_img)

        event_imgs =[self.create_event(event) for event in events]
        event_seps = [self.event_sep] * len(event_imgs)
        self.content.extend([img for pair in zip(event_imgs, event_seps)
                                 for img in pair][:-1])

    def create_event(self, event):
        event['datetime'] = '{} {}'.format(event['date'], event['time'])
        event['address'] = event['address1'] + '\n' + event['address2']

        item_file = os.path.join(self.template_path, 'item.png')
        event_img = ImagePiece.from_file(item_file)
        for field in self.TXT_FIELDS:
            event_img.draw_text(event[field], self.text_style[field])

        avatar_file = util.get_file(self.avatars_path, event['presenter_name'])
        if not avatar_file:
            raise('No avatar file found for {}'.format(event['presenter_name']))
        avatar_img = ImagePiece.from_file(avatar_file)
        avatar_img.to_circle_thumbnail(tuple(self.img_style['avatar']['size']))

        composer = ImageComposer([event_img, avatar_img])
        composer.zstack(self.img_style['avatar']['start'])
        composer.save('event.png')
        return composer.to_img_piece()

    def compose(self):
        self.content.append(self.tail)
        composer = ImageComposer(self.content)
        composer.vstack()
        return composer.save('./new_post.png')


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
        events = sheet_service.read_as_map(self.config['EVENT_FILE_ID'], 2, 10)
        events = sorted(events, key=lambda k: k['date'])
        self.create_poster(events, ['Generalized Mining', 'Consensus'])


def main():
    app = WhitepaperJournal()
    app.run()


if __name__ == '__main__':
    main()
