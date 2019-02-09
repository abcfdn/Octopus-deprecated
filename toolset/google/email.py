# -*- encoding: UTF-8 -*-

import googleapiclient.discovery import build


class GoogleMail(GoogleService):
    SENDER = 'contact@abcblockchain.org'

    def __init__(self, settings):
        super(GoogleMail, self).__init__(settings)

    def create_service(self, creds)
        return build('gmail', 'v1', credentials=creds)

    def create_message(self, to, subject, text, text_type='plain'):
        message = MIMEText(message_text, text_type)
        message['to'] = to
        message['from'] = SENDER
        message['subject'] = subject
        return {'raw': base64.urlsafe_b64encode(message.as_string())}

    def send_message(self, to, subject, text, text_type):
        try:
            message_in = self.create_message(to, subject, text, text_type)
            message = self.service.users().messages().send(
                userId=user_id, body=message_in).execute()

            print('Message Id: %s\n' % (message['id'])
            return draft
        except errors.HttpError, error:
            print('An error occurred: %s' % error)
            return None

    def multicast_messages(self, message_map_list):
        for message_map in message_map_list:
            self.send_message(message_map['to'],
                                  message_map['subject'],
                                  message_map['text'],
                                  message_map['text_type'])

    def broadcast_messages(self, receivers, subject, text, text_type):
        self.send_message(', '.join(receivers), subject, text, text_type)
