from io import StringIO
from urllib.parse import urlunsplit, urlencode

import requests
from lxml.html import parse


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


def extract_links(doc, css_selector):
    elements = doc.cssselect(css_selector)
    try:
        return [link.attrib.get('href') for link in elements if link.attrib.get('href')]
    except (IndexError, AttributeError, KeyError) as e:
        raise LinksError('No links') from e


class BaseParser:
    scheme = None
    netloc = None
    path = None
    query_param = None
    item_selector = None
    next_page_selector = None
    captcha_selector = None

    def __init__(self, count, recursion):
        self.count = count
        self.recursion = bool(recursion)
        self.session = requests.session()
        self.links = []
        self.doc = None
        self.recursion_start = 0

    def _build_init_url(self, query):
        url = urlunsplit((
            self.scheme,
            self.netloc,
            self.path,
            urlencode({self.query_param: query}),
            ''
        ))
        return url

    def _get_next_page_url(self):
        try:
            url = extract_links(self.doc, self.next_page_selector)[0]
            return url
        except LinksError as e:
            raise NextPageError('No next page') from e

    def _is_captcha_checking(self):
        is_captcha = self.doc.cssselect(self.captcha_selector)
        if bool(is_captcha):
            raise CaptchaError

    def _make_request(self, url):
        response = self.session.get(url, headers=browser_header)

        if response.status_code == 200:
            self.doc = parse(StringIO(response.text)).getroot()
            self.doc.make_links_absolute(url)
            return True

        return False

    def linear_search(self):
        url = self._get_next_page_url()
        if self._make_request(url):
            if self.captcha_selector:
                self._is_captcha_checking()
            self.links.extend(
                extract_links(self.doc, self.item_selector)
            )

    def recursive_search(self):
        page = slice(self.recursion_start, len(self.links) - 1)
        for link in self.links[page]:
            r = self.session.get(link, headers=browser_header)
            if r.status_code == 200:
                doc = parse(StringIO(r.text)).getroot()
                doc.make_links_absolute(link)
                pl = extract_links(doc, 'a')
                self.links.extend(set(pl))
            if len(self.links) >= self.count:
                return

        self.recursion_start = len(self.links)
        self.linear_search()

    def search(self, query):
        url = self._build_init_url(query)
        if self._make_request(url):
            if self.captcha_selector:
                self._is_captcha_checking()
            self.links.extend(
                extract_links(self.doc, self.item_selector)
            )

        while len(self.links) < self.count:
            if self.recursion:
                self.recursive_search()
            else:
                self.linear_search()

        return self.links[:self.count]
