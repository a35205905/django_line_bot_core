from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from linebot import WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from .services import handle_event

import logging

PARSER = WebhookParser(settings.LINE_CHANNEL_SECRET)

LOGGER = logging.getLogger(settings.LOGGING_ROLE)


@csrf_exempt
def callback(request):
    # 確認是否為POST
    if request.method != 'POST':
        return HttpResponseBadRequest()

    signature = request.META['HTTP_X_LINE_SIGNATURE']
    body = request.body.decode('utf-8')
    # 確認Request來自LINE Server
    try:
        events = PARSER.parse(body, signature)
    # 不是從來自LINE Server
    except InvalidSignatureError:
        return HttpResponseForbidden()
    # LINE Server其他問題
    except LineBotApiError:
        return HttpResponseBadRequest()

    for event in events:
        handle_event(event)

    return HttpResponse()
