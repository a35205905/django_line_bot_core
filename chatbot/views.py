from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, PostbackEvent, TextSendMessage

import logging

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

logger = logging.getLogger(settings.LOGGING_ROLE)


@csrf_exempt
def callback(request):
    # 確認是否為POST
    logger.debug(request.method)
    if request.method != 'POST':
        return HttpResponseBadRequest()

    signature = request.META['HTTP_X_LINE_SIGNATURE']
    body = request.body.decode('utf-8')
    # 確認Request來自LINE Server
    try:
        events = parser.parse(body, signature)
    # 不是從來自LINE Server
    except InvalidSignatureError:
        return HttpResponseForbidden()
    # LINE Server其他問題
    except LineBotApiError:
        return HttpResponseBadRequest()

    for event in events:
        # 處理Post資料
        if isinstance(event, PostbackEvent):
            pass
        # 處理訊息
        elif isinstance(event, MessageEvent):
            # 處理文字
            if isinstance(event.message, TextMessage):
                text = event.message.text.strip()
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=text)
                )
    return HttpResponse()
