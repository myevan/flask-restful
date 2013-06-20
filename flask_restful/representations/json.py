from __future__ import absolute_import

from flask import make_response, current_app, request
from json import dumps

from werkzeug.http import HTTP_STATUS_CODES

import re
import difflib

# This dictionary contains any kwargs that are to be passed to the json.dumps
# function, used below.
settings = {
    'ensure_ascii' : False,
    'encoding' : 'utf-8',
}

def error_json(e):
    code = getattr(e, 'code', 500)
    data = getattr(e, 'data', error_data(code))

    if code >= 500:
        current_app.logger.exception("Internal Error")

    if code == 404 and ('message' not in data or
                        data['message'] == HTTP_STATUS_CODES[404]):
        rules = dict([(re.sub('(<.*>)', '', rule.rule), rule.rule)
                      for rule in current_app.url_map.iter_rules()])
        close_matches = difflib.get_close_matches(request.path, rules.keys())
        if close_matches:
            # If we already have a message, add punctuation and continue it.
            if "message" in data:
                data["message"] += ". "
            else:
                data["message"] = ""

            data['message'] += 'You have requested this URI [' + request.path + \
                    '] but did you mean ' + \
                    ' or '.join((rules[match]
                                 for match in close_matches)) + ' ?'

    resp = output_json(data, code)

    if code == 401:
        resp = unauthorized(resp,
            current_app.config.get("HTTP_BASIC_AUTH_REALM", "flask-restful"))

    return resp

def output_json(data, code, headers=None):
    """Makes a Flask response with a JSON encoded body"""

    # If we're in debug mode, and the indent is not set, we set it to a
    # reasonable value here.  Note that this won't override any existing value
    # that was set.  We also set the "sort_keys" value.
    local_settings = settings.copy()
    if current_app.debug:
        local_settings.setdefault('indent', 4)
        local_settings.setdefault('sort_keys', True)

    # We also add a trailing newline to the dumped JSON if the indent value is
    # set - this makes using `curl` on the command line much nicer.
    dumped = dumps(data, **local_settings)
    if 'indent' in local_settings:
        dumped += '\n'

    resp = make_response(dumped, code)
    resp.headers.extend(headers or {})

    # broken utf8 string display bug fix on chrome browser
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    return resp


def error_data(code):
    """Constructs a dictionary with status and message for returning in an
    error response"""
    error = {
        'status': code,
        'message': http_status_message(code),
    }
    return error

def http_status_message(code):
    """Maps an HTTP status code to the textual status"""
    return HTTP_STATUS_CODES.get(code, '')

def unauthorized(response, realm):
    """ Given a response, change it to ask for credentials"""
    response.headers['WWW-Authenticate'] = challenge("Basic", realm)
    return response

