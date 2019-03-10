# -*- encoding: UTF-8 -*-

import os
import logging

import toolset.utils.util as util
from toolset.google.sheet import GoogleSheet

from apps.constants import MEMBERSHIP_APP
from apps.base import Task

logger = logging.getLogger('membership_base')

class MembershipBase(Task):
    NUM_OF_ROWS_TO_READ = 1000

    def __init__(self, common_config):
        super().__init__(common_config)
        self.load_members()

    def app_name(self):
        return MEMBERSHIP_APP

    def load_members(self):
        sheet_service = GoogleSheet(self.config['google'])
        self.members = sheet_service.read_as_map(
            self.config['data']['members']['remote'],
            'Form Responses 1',
            (2, self.NUM_OF_ROWS_TO_READ + 1))
