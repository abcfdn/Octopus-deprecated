# -*- encoding: UTF-8 -*-

import logging

from googleapiclient.discovery import build
from .service import GoogleService

logger = logging.getLogger('google_sheet')


class GoogleSheet(GoogleService):
    HEADER_RANGE = "{}!1:1"

    def __init__(self, settings):
        super().__init__(settings)

    def create_service(self, creds):
        return build('sheets',
                     'v4',
                     credentials=creds,
                     cache_discovery=False)

    def read(self, file_id, range_name):
        return self.service.spreadsheets().values().get(
            spreadsheetId=file_id, range=range_name).execute()

    def read_header(self, file_id, sheet_name):
        fields = self.read(file_id, '{}!1:1'.format(sheet_name)).get('values')
        if not len(fields) or not len(fields[0]):
            logging.warning("No data found")
            return []
        # Project Name (blablabla) => project_name
        return [field.split('(')[0].strip().lower().replace(' ', '_')
                for field in fields[0] if field]

    def read_as_map(self, file_id, sheet_name, row_range):
        fields = self.read_header(file_id, sheet_name)
        results = self.read(file_id, '{}!{}:{}'.format(
            sheet_name, row_range[0], row_range[1]))
        return [dict(zip(fields, row[0:len(fields)]))
                for row in results.get('values')]
