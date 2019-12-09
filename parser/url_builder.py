from urllib.parse import urlunsplit, urlencode


class URLBuilder:
    scheme = 'https'
    netloc = None
    path = None
    result = None

    def __init__(self, netloc: str, path: str, query: dict, **kwargs) -> None:
        query_str = urlencode(query)

        self.result = urlunsplit((
            kwargs.get('scheme', self.scheme),
            netloc,
            path,
            query_str,
            kwargs.get('fragment', ''),
        ))

    def url(self) -> str:
        return self.result
