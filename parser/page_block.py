from .exceptions import CssSelectorNotSpecified


class HtmlBlock:
    css_selector = None

    def __init__(self, doc, **kwargs):
        if kwargs.get('css_selector'):
            self.css_selector = kwargs.get('css_selector')

        if not self.css_selector:
            raise CssSelectorNotSpecified

        self.elements = doc.cssselect(self.css_selector)

    def is_present(self):
        return bool(self.css_selector)

    def do_work(self):
        return self.elements
