import urllib, urllib2
import json
from django.utils.translation import ugettext as _
from recaptcha2 import DEFAULT_API_SSL_SERVER

CAPTCHA_ERROR_CODE = {
    'no-required': _('This field is required.'),
    'no-network': _('Network problem.'),
    'no-decode': _('Error during response decoding.'),
    'missing-input-secret': _('The secret parameter is missing.'),
    'invalid-input-secret': _('The secret parameter is invalid or malformed.'),
    'missing-input-response': _('The response parameter is missing.'),
    'invalid-input-response': _('The response parameter is invalid or malformed.'),
}


class ReCaptcha2Response():
    def __init__(self, is_clean=False, error_code='unknown'):
        self.is_clean = is_clean
        self.error_code = error_code


def validate_captcha(recaptcha_response, private_key):
    url = "%s/api/siteverify" % DEFAULT_API_SSL_SERVER

    if not recaptcha_response:
        return ReCaptcha2Response(error_code='no-required')

    params = urllib.urlencode({
                              'secret': private_key,
                              'response':  recaptcha_response,
                              #'remoteip':'' #not support now
                              })

    request = urllib2.Request(
        url=url,
        data=params,
        headers={"Content-type": "application/x-www-form-urlencoded", "User-agent": "reCAPTCHA Python"}
        )

    return_str = ''
    try:
        response = urllib2.urlopen(request)
        response_str = response.read()
        response.close()
    except:
        return ReCaptcha2Response(error_code='no-network')

    try:
        response = json.loads(response_str)
        if response.get('success', False) is True or response.get('success', 'false') == "true":
            return ReCaptcha2Response(is_clean=True)
        else:
            error_code = response.get('error-code', ['unknown'])
            if error_code:
                return ReCaptcha2Response(error_code=error_code[0])
            else:
                return ReCaptcha2Response()
    except:
       return ReCaptcha2Response(error_code='no-decode')


def get_error_message(code):
    return CAPTCHA_ERROR_CODE.get(code, _('Unknown captcha error'))