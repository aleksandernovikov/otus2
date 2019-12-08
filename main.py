import argparse
from pprint import pprint

from parser.base import BaseParser
from parser.page_block import HtmlBlock


class YaItemsBlock(HtmlBlock):
    css_selector = 'li.serp-item > div.organic a.link.organic__url'


class YaNextPageBlock(HtmlBlock):
    css_selector = 'div.pager > a.pager__item_kind_next'


class YaCaptchaBlock(HtmlBlock):
    css_selector = 'form.form_error_no'


class YandexParser(BaseParser):
    scheme = 'https'
    netloc = 'yandex.ru'
    path = 'search'
    query_param = 'text'
    item_selector = 'li.serp-item > div.organic a.link.organic__url'
    next_page_selector = 'div.pager > a.pager__item_kind_next'
    captcha_selector = 'form.form_error_no'


class GoogleParser(BaseParser):
    scheme = 'https'
    netloc = 'google.com'
    path = 'search'
    query_param = 'q'
    item_selector = 'div.g > div > div.rc > div.r > a'
    next_page_selector = 'table#nav td.navend > a'


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


if __name__ == '__main__':
    params = parse_arguments()

    parsers_map = {
        'yandex': YandexParser,
        'google': GoogleParser
    }
    selected_parser = parsers_map.get(params.search_engine)
    parser = selected_parser(params.count, params.recursive)

    links = parser.search(params.query)
    print(f'links={len(links)}')
    pprint(links)
