import argparse
import webbrowser
from io import StringIO
from pprint import pprint
from random import choice
from time import sleep
from urllib.parse import urlunsplit, urlencode, urljoin
from lxml.html import parse

import requests


class NextPageError(Exception):
    pass


class LinksError(Exception):
    pass


class CaptchaError(Exception):
    pass


browser_header = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0',
    'Accept': 'text/css,*/*;q=0.1',
    'Accept-Language': 'ru,en-US;q=0.7,en;q=0.3',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
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
    parser.add_argument('-C', '--count', type=int, default=20, help='Links count')
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
    next_page_selector = 'div.pager > a.pager__item_kind_next'

    def __init__(self, count, recursive):
        self.count = count
        self.recursive = bool(recursive)
        self.session = requests.session()
        self.links = []
        self.doc = None
        self.current_url = None

    def _build_init_url(self, query):
        url = urlunsplit((
            self.scheme,
            self.netloc,
            self.path,
            urlencode({self.query_param: query}),
            ''
        ))
        return url

    def _extract_links_by_selector(self, selector):
        link_list = self.doc.cssselect(selector)
        try:
            return [link.attrib['href'] for link in link_list]
        except KeyError as e:
            raise LinksError('No links') from e

    def _get_next_page_url(self):
        print('_get_next_page_url')
        self.doc.make_links_absolute(self.current_url)
        next_page_url = self.doc.cssselect(self.next_page_selector)
        try:
            return next_page_url[0].attrib['href']
        except (IndexError, AttributeError, KeyError) as e:
            raise NextPageError('No next page') from e

    def _solve_captcha(self):
        try:
            captcha_form = self.doc.cssselect('form.form_error_no')[0]
            img = self.doc.cssselect('div.captcha__image > img')
            webbrowser.open(img[0].attrib['src'], new=0, autoraise=True)
            params = dict(
                key=captcha_form.cssselect('input.form__key')[0].attrib['value'],
                retpath=captcha_form.cssselect('input.form__retpath')[0].attrib['value']
            )
            pprint(params)
            params['rep'] = input('Input your captcha decision:')
            # TODO  нужно добавить get параметр с captcha_decision к captcha_url
            action_url = captcha_form.attrib['action']
            captcha_url = urljoin(self.current_url, action_url)
            captcha_url = urljoin(captcha_url, '?' + urlencode(params))
            print(captcha_url)
            response = self.session.get(captcha_url)
            print(response.status_code)
            print(response.text)
        except Exception as e:
            print(e)

    def _is_captcha_checking(self):
        captcha_form = self.doc.cssselect('form.form_error_no')
        if bool(captcha_form):
            raise CaptchaError

    def _make_request(self, url):
        self.current_url = url
        response = self.session.get(self.current_url, headers=browser_header)

        if response.status_code == 200:
            self.doc = parse(StringIO(response.text)).getroot()
            print(response.text)
            if self._is_captcha_checking():
                return False
            return True

        return False

    def search(self, query):
        url = self._build_init_url(query)
        if self._make_request(url):
            self.links.extend(self._extract_links_by_selector(self.item_selector))
        sleep(choice(range(3, 10)))

        while len(self.links) < self.count:
            url = self._get_next_page_url()
            sleep(choice(range(3, 10)))
            if self._make_request(url):
                self.links.extend(self._extract_links_by_selector(self.item_selector))
            print(f'links={len(self.links)}')

        return self.links


if __name__ == '__main__':
    params = parse_arguments()
    print(params)
    s = YandexParser(params.count, params.recursive)
    links = s.search(params.query)
    print(links)
