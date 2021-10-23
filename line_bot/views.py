from re import template
from types import new_class
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookHandler, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, MessageTemplateAction, ButtonsTemplate

from .scraper import Scrape

line_bot_api = LineBotApi('key')
parser = WebhookParser('key')


@csrf_exempt
def callback(request):
 
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
 
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
 
        for event in events:

            if isinstance(event, MessageEvent):
                
                stock_number = Scrape(event.message.text)
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=stock_number.get_web())
                )

        return HttpResponse()

    else:
        return HttpResponseBadRequest()
