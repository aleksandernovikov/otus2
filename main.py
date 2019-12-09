import argparse
from pprint import pprint
from random import sample

from parser.base import BlockBaseParser
from parser.page_block import HtmlBlock
from parser.random_user_agent import RandomUserAgentHeader
from parser.url_builder import URLBuilder


class GoogleItemsBlock(HtmlBlock):
    css_selector = 'div.g > div > div.rc > div.r > a'


class GoogleNextPageBlock(HtmlBlock):
    css_selector = 'table#nav td.navend > a'


class GoogleParser(BlockBaseParser):
    blocks: list = [
        GoogleItemsBlock,
        GoogleNextPageBlock,
    ]

    def __init__(self, count: int, recursive: bool):
        super().__init__()

        self.count = count
        self.recursive = recursive

    def search(self, query: str) -> list:
        init_url = URLBuilder(netloc='google.com', path='search', query={'q': query}).url()

        r = self.do_work(init_url)
        links = [link.attrib.get('href') for link in r['GoogleItemsBlock'] if link.attrib.get('href')]
        print(links)
        return links


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
    header = RandomUserAgentHeader(
        user_agents_list=['Mozilla / 5.0(X11; Ubuntu; Linux x86_64; rv: 70.0) Gecko / 20100101 Firefox / 70.0']
    )
    pprint(header.get_ua())

    params = parse_arguments()

    parsers_map = {
        'google': GoogleParser
    }
    selected_parser = parsers_map.get(params.search_engine)
    parser = selected_parser(params.count, params.recursive)

    q_vars = [
        'нормальный',
        'пример',
        'человек',
        'плохой',
        'хороший'
    ]

    query = " ".join(sample(q_vars, 2))

    links = parser.search(query)
    print(f'links={len(links)}')
    pprint(links)
