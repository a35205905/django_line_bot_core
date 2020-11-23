from linebot.models.events import MessageEvent, PostbackEvent
from linebot.models.messages import TextMessage, LocationMessage
from django.conf import settings
from .chatbots import TextMessageChatbot, LocationMessageChatbot

import logging

LOGGER = logging.getLogger(settings.LOGGING_ROLE)


def handle_event(event):
    # 處理Post資料
    if isinstance(event, PostbackEvent):
        pass
    # 處理訊息
    elif isinstance(event, MessageEvent):
        # 處理文字
        if isinstance(event.message, TextMessage):
            chatbot = TextMessageChatbot(event)
        # 處理定位
        elif isinstance(event.message, LocationMessage):
            chatbot = LocationMessageChatbot(event)

    if chatbot:
        chatbot.handle_event()
        chatbot.reply_message()
