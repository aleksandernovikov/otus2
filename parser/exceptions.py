class NextPageError(Exception):
    pass


class LinksError(Exception):
    pass


class CaptchaError(Exception):
    pass


class CssSelectorNotSpecified(Exception):
    """
    no css selector specified
    """
    pass
