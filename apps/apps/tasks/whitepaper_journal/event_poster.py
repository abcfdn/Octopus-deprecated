# -*- encoding: UTF-8 -*-

import os
import logging

from datetime import datetime
from toolset.image.composer import ImageComposer, ImagePiece
from toolset.google.sheet import GoogleSheet
import toolset.utils.util as util
from apps.base import Task

logger = logging.getLogger('whitepaper_journal_event_poster')


class WhitepaperJournalPoster(Task):
    def __init__(self, common_config):
        super().__init__(common_config)
        self.txt_style = self.config['txt_style']
        self.img_style = self.config['img_style']

    def reset(self):
        self.header = self.get_common_template('header.png')
        self.keywords = self.get_common_template('meetup_keywords.png')
        self.meetup = self.get_common_template('meetup.png')
        self.tail = self.get_common_template('tail.png')

        self.content = [self.header, self.keywords, self.meetup]

    def process(self, args):
        self.reset()
        self.content.append(self.tail)
        composer = ImageComposer(self.content)
        composer.vstack()
        self.save(composer)

