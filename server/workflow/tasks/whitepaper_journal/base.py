# -*- encoding: UTF-8 -*-

import calendar
import dateparser
from datetime import datetime, timedelta

from server.workflow.base import Task
from server.workflow.constants import WHITEPAPER_JOURNAL_APP
from server.platforms.google.sheet import GoogleSheet
import server.platforms.utils.util as util

from server.db.service import Service

class WhitepaperJournalBase(Task):
    NUM_OF_ROWS_TO_READ = 1000
    FIELDS_TO_COMPARE = ['session_name', 'presenter_name']

    def __init__(self):
        super().__init__(google_creds)
        self.service = Service(self.config['mongo'])

    def app_name(self):
        return WHITEPAPER_JOURNAL_APP

    def get_session(self, session_id):
        self.service.get_session(session_id)

    def get_presenter(self, email):
        self.service.get_presenter(session_id)

    def process(self, args):
        raise('Not Implemented')
