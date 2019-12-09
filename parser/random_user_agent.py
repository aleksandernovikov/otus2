from collections import OrderedDict
from random import choice


class RandomUserAgentHeader:
    ua_header = OrderedDict([
        ('User-Agent', ''),
        ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
        ('Accept-Language', 'ru,en-US;q=0.7,en;q=0.3'),
        ('DNT', '1'),
        ('Connection', 'keep-alive'),
        # Cookie
        ('Upgrade-Insecure-Requests', '1'),
        ('Pragma', 'no-cache'),
        ('Cache-Control', 'no-cache'),
        ('TE', 'Trailers')
    ])
    ua_list = ['Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0']

    def __init__(self, user_agents_list: list = None):
        self.ua_list.extend(user_agents_list)

    def get_ua(self):
        self.ua_header['User-Agent'] = choice(self.ua_list)
        # print(self.ua_header['User-Agent'])
        return self.ua_header
