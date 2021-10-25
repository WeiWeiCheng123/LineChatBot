from re import template
from types import new_class
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookHandler, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, MessageTemplateAction, ButtonsTemplate, FlexSendMessage, flex_message
from requests.models import DEFAULT_REDIRECT_LIMIT

from .scraper import Scrape

line_bot_api = LineBotApi('aUDAN6kht26+7QFf7ErvmRpxmSE90o9Fibc9mdW+4D1/Ze5a2qbWmNMgpar1aAc6eT7seAu3o6O9fKAgJ77J36otL6k+qWWlTzRn6mvw+/Rgci3w0jdOalVKkqDJtb1KrrmCrGkgyzfTKxBiCQRS5AdB04t89/1O/w1cDnyilFU=')
parser = WebhookParser('14a3dd48481e6f2beb2396d76f1ce08c')

flex_message = {"type": "carousel", "contents": [{"type": "bubble", "header": {"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": "123", "size": "lg"}]}, "body": {"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": "123", "margin": "none", "size": "md", "wrap": True}, {"type": "text", "text": "123", "wrap": True, "maxLines": 5, "size": "sm"}]}, "footer": {"type": "box", "layout": "vertical", "contents": [{"type": "button", "action": {"type": "uri", "label": "\u9ede\u6211\u770b\u66f4\u591a", "uri": "123"}}]}, "styles": {"header": {"backgroundColor": "#b6cde2"}}}, {"type": "bubble", "header": {"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": "123", "size": "lg"}]}, "body": {"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": "123", "wrap": True}, {"type": "text", "text": "123", "size": "sm", "wrap": True, "maxLines": 5}]}, "footer": {"type": "box", "layout": "vertical", "contents": [{"type": "button", "action": {"type": "uri", "label": "\u9ede\u6211\u770b\u66f4\u591a", "uri": "123"}}]}, "styles": {"header": {"backgroundColor": "#b6cde2"}}}, {"type": "bubble", "header": {"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": "123", "size": "lg", "wrap": True}]}, "body": {"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": "123", "wrap": True}, {"type": "text", "text": "123", "maxLines": 5, "wrap": True, "size": "sm"}]}, "footer": {"type": "box", "layout": "vertical", "contents": [{"type": "button", "action": {"type": "uri", "label": "\u9ede\u6211\u770b\u66f4\u591a", "uri": "123"}}]}, "styles": {"header": {"backgroundColor": "#b6cde2"}}}, {"type": "bubble", "header": {"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": "123", "size": "lg"}]}, "body": {"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": "123", "wrap": True}, {"type": "text", "text": "123", "size": "sm", "wrap": True, "maxLines": 5}]}, "footer": {"type": "box", "layout": "vertical", "contents": [{"type": "button", "action": {"type": "uri", "label": "\u9ede\u6211\u770b\u66f4\u591a", "uri": "123"}}]}, "styles": {"header": {"backgroundColor": "#b6cde2"}}}, {"type": "bubble", "header": {"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": "123", "size": "lg"}]}, "body": {"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": "123", "wrap": True}, {"type": "text", "text": "123", "maxLines": 5, "size": "sm", "wrap": True}]}, "footer": {"type": "box", "layout": "vertical", "contents": [{"type": "button", "action": {"type": "uri", "label": "\u9ede\u6211\u770b\u66f4\u591a", "uri": "123"}}]}, "styles": {"header": {"backgroundColor": "#b6cde2"}}}]}

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
                if stock_number.real_stock():
                    stock_name, news_list, news_link, content = stock_number.get_web()
                    for i in range(5):
                        flex_message['contents'][i]['header']['contents'][0]['text'] = stock_name
                        flex_message['contents'][i]['body']['contents'][0]['text'] = news_list[i]
                        flex_message['contents'][i]['footer']['contents'][0]['action']['uri'] = news_link[i]
                        flex_message['contents'][i]['body']['contents'][1]['text'] = content[i]
                    line_bot_api.reply_message(
                        event.reply_token,
                        FlexSendMessage('股市新聞',flex_message)
                    )
                else:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=stock_number.get_web())
                    )
        return HttpResponse()

    else:
        return HttpResponseBadRequest()