from werkzeug.http import HTTP_STATUS_CODES


def challenge(authentication, realm):
    """Constructs the string to be sent in the WWW-Authenticate header"""
    return u"{0} realm=\"{1}\"".format(authentication, realm)


def unpack(value):
    """Return a three tuple of data, code, and headers"""
    if not isinstance(value, tuple):
        return value, 200, {}

    try:
        data, code, headers = value
        return data, code, headers
    except ValueError:
        pass

    try:
        data, code = value
        return data, code, {}
    except ValueError:
        pass

    return value, 200, {}
