import re

from django.conf import settings
from django.template.response import TemplateResponse

from rpgsite.tools import GetSetting


class HideIndentMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if isinstance(response, TemplateResponse):
            text = response.content.decode()
            text = re.sub(r'\n\s+', '\n', text)
            response.content = text.encode()
        return response

class PrettyIndentMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from bs4 import BeautifulSoup
        response = self.get_response(request)
        if isinstance(response, TemplateResponse):
            text = response.content.decode()
            soup = BeautifulSoup(text, GetSetting('BEAUTIFULSOUP_PARSER'))
            prettyHTML = soup.prettify()
            response.content = prettyHTML.encode()
        return response