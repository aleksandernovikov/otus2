import pytest
from requests import Session, Response

from parser.base import BaseParser


@pytest.fixture
def web_response(monkeypatch):
    def se_response(*args, **kwargs):
        content = None
        with open('ya.html') as f:
            content = f.read()
        response = Response()
        response.status_code = 200
        response._content = bytearray(content, 'utf8')
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

    def test_make_request(self, web_response):
        self.bp.scheme = 'https'
        self.bp.netloc = 'yandex.ru'
        self.bp.path = 'search'
        self.bp.query_param = 'text'
        url = self.bp._build_init_url('pytest')

        response = self.bp._make_request(url)
