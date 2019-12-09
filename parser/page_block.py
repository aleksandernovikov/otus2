from .exceptions import CssSelectorNotSpecified


class HtmlBlock:
    css_selector: str = None

    def __init__(self, document, **kwargs) -> None:
        if kwargs.get('css_selector'):
            self.css_selector = kwargs.get('css_selector')

        if not self.css_selector:
            raise CssSelectorNotSpecified

        self.elements = document.cssselect(self.css_selector)

    def is_present(self) -> bool:
        return bool(self.elements)

    def do_work(self) -> list:
        return self.elements
