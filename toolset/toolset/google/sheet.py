# -*- encoding: UTF-8 -*-

from googleapiclient.discovery import build
from .service import GoogleService

logger = logging.getLogger('google_sheet')


class GoogleSheet(GoogleService):
    HEADER_RANGE = "Schedule!1:1"

    def __init__(self, settings):
        super().__init__(settings)

    def create_service(self, creds):
        return build('sheets', 'v4', credentials=creds)

    def read(self, sheet_id, range_name):
        return self.service.spreadsheets().values().get(
            spreadsheetId=sheet_id, range=range_name).execute()

    def read_header(self, sheet_id):
        fields = self.read(sheet_id, self.HEADER_RANGE).get('values')
        if not len(fields) or not len(fields[0]):
            logging.warning("No data found")
            return []
        # Project Name => project_name
        return [field.lower().replace(' ', '_') for field in fields[0]]

    def read_as_map(self, sheet_id, start_row, end_row):
        fields = self.read_header(sheet_id)
        results = self.read(sheet_id, 'Schedule!{}:{}'.format(start_row, end_row))
        return [dict(zip(fields, row[0:len(fields)]))
                for row in results.get('values')]
