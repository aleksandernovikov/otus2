from .exceptions import LinksError


def extract_links(doc, css_selector):
    elements = doc.cssselect(css_selector)
    try:
        return [link.attrib.get('href') for link in elements if link.attrib.get('href')]
    except (IndexError, AttributeError, KeyError) as e:
        raise LinksError('No links') from e
