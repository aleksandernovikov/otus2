import pytest
from requests import Session, Response

from parser.base import BaseParser, extract_links

yandex_page_content = None
with open('ya.html') as f:
    yandex_page_content = f.read()


@pytest.fixture
def web_response(monkeypatch):
    def se_response(*args, **kwargs):
        response = Response()
        response.status_code = 200
        response._content = bytearray(yandex_page_content, 'utf8')
        return response

    monkeypatch.setattr(Session, 'get', se_response)


class TestBaseParser:
    def setup(self):
        self.bp = BaseParser(10, True)

    def test_build_init_url(self):
        self.bp.scheme = 'https'
        self.bp.netloc = 'yandex.ru'
        self.bp.path = 'search'
        self.bp.query_param = 'text'
        url = self.bp._build_init_url('pytest')

        assert url == 'https://yandex.ru/search?text=pytest'

    def test_make_request(self):
        self.bp.scheme = 'https'
        self.bp.netloc = 'yandex.ru'
        self.bp.path = 'search'
        self.bp.query_param = 'text'
        url = self.bp._build_init_url('pytest')

        result = self.bp._make_request(url)
        assert result is True


def test_extract_links():
    bp = BaseParser(10, True)
    bp.scheme = 'https'
    bp.netloc = 'yandex.ru'
    bp.path = 'search'
    bp.query_param = 'text'
    url = bp._build_init_url('pytest')

    bp._make_request(url)
    links = extract_links(bp.doc, 'li.serp-item > div.organic a.link.organic__url')
    assert isinstance(links, list)


class YandexParser(BaseParser):
    scheme = 'https'
    netloc = 'yandex.ru'
    path = 'search'
    query_param = 'text'
    item_selector = 'li.serp-item > div.organic a.link.organic__url'
    next_page_selector = 'div.pager > a.pager__item_kind_next'
    captcha_selector = 'form.form_error_no'


class TestLenearYandexParser:
    parser = YandexParser(10, False)

    def test_search(self):
        result = self.parser.search('pytest')
        assert isinstance(result, list)
        assert len(result)
