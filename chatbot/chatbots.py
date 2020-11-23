from linebot import LineBotApi
from linebot.models.sources import SourceGroup, SourceRoom
from linebot.models.send_messages import TextSendMessage, QuickReply, QuickReplyButton
from linebot.models.actions import LocationAction
from django.conf import settings

import logging

LOGGER = logging.getLogger(settings.LOGGING_ROLE)


class Chatbot:
    def __init__(self, event, user_id=None, group_id=None, room_id=None, reply_token=None):
        self.event = event
        self.user_id = user_id
        self.group_id = group_id
        self.room_id = room_id
        self.reply_token = reply_token
        self.line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

    def handle_event(self):
        self.user_id = self.event.source.user_id
        if isinstance(self.event.source, SourceGroup):
            self.group_id = self.event.source.group_id
        elif isinstance(self.event.source, SourceRoom):
            self.room_id = self.event.source.room_id
        self.reply_token = self.event.reply_token

    def reply_message(self):
        self.line_bot_api.reply_message(self.reply_token, self.get_reply_messages())

    def get_reply_messages(self):
        LOGGER.debug('reply_messages')


class MessageChatbot(Chatbot):
    def __init__(self, event, message=None):
        super().__init__(event)
        self.message = message

    def handle_event(self):
        super().handle_event()
        self.message = self.event.message


class TextMessageChatbot(MessageChatbot):
    def __init__(self, event, text=None):
        super().__init__(event)
        self.text = text

    def handle_event(self):
        super().handle_event()
        self.text = self.event.message.text.strip()

    def get_reply_messages(self):
        text_functions = {
            '打卡': 'check_in',
            '嗨': 'hello',
            '首頁': 'index',
        }
        text_function = text_functions.get(self.text)
        if text_function:
            return getattr(self, text_function)()
        else:
            return TextSendMessage(text=self.text)

    @staticmethod
    def check_in():
        return TextSendMessage(
            text='請點選打卡按鈕',
            quick_reply=QuickReply(items=[
                QuickReplyButton(action=LocationAction(label='打卡'))
            ])
        )

    def hello(self):
        return TextSendMessage(
            text='我所在的群組為{group_id}\n我的使用者身份為{user_id}'.format(
                user_id=self.user_id,
                group_id=self.group_id
            )
        )

    @staticmethod
    def index():
        return TextSendMessage(
            text='https://liff.line.me/1655260637-Dlg2wBRp'
        )


class LocationMessageChatbot(MessageChatbot):
    def __init__(self, event, address=None):
        super().__init__(event)
        self.address = address

    def handle_event(self):
        super().handle_event()
        self.address = self.message.address

    def get_reply_messages(self):
        messages = [
            TextSendMessage(text='打卡成功'),
            TextSendMessage(text=self.address)
        ]
        return messages
