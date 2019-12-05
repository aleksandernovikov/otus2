import argparse
from io import StringIO
from urllib.parse import urlunsplit, urlencode
from lxml.html import parse

import requests

browser_header = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 '
                  'YaBrowser/17.1.1.773 (beta) Yowser/2.5 Safari/537.36',
    'Accept-Language': 'ru,en;q=0.8',
}


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog='otus-search',
        description='Программа находит в интернете начиная от стартовой точки все ссылки '
                    'на веб-странице и выводит в терминал ',
        usage='%(prog)s [options]',
        allow_abbrev=True
    )

    parser.add_argument(
        'query',
        type=str,
        help='Input your search request'
    )
    parser.add_argument('-S', '--search_engine',
                        type=str,
                        choices=['google', 'yandex'],
                        default='google',
                        help='Search engine'
                        )
    parser.add_argument('-C', '--count', type=int, default=42, help='Links count')
    parser.add_argument(
        '-R', '--recursive',
        type=int,
        choices=[0, 1],
        default=0, help='Recursive search')

    return parser.parse_args()


class YandexParser:
    scheme = 'https'
    netloc = 'yandex.ru'
    path = 'search'
    query_param = 'text'
    item_selector = 'li.serp-item > div.organic a.link.organic__url'

    def __init__(self, count, recursive):
        self.count = count
        self.recursive = bool(recursive)
        self.session = requests.session()

    def _build_url(self, query):
        url = urlunsplit((
            self.scheme,
            self.netloc,
            self.path,
            urlencode({self.query_param: query}),
            ''
        ))
        return url

    def _get_links(self, page_content):
        doc = parse(StringIO(page_content)).getroot()
        links = doc.cssselect(self.item_selector)
        print([link.attrib['href'] for link in links])

    def search(self, query):
        url = self._build_url(query)
        response = self.session.get(url)
        self._get_links(response.text)


if __name__ == '__main__':
    params = parse_arguments()
    print(params)
    s = YandexParser(params.count, params.recursive)
    s.search(params.query)
