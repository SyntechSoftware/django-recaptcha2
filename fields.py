import sys

from django import forms
from django.conf import settings
from django.forms.fields import ValidationError
from django.utils.translation import ugettext_lazy as _

from recaptcha2.captcha import validate_captcha, get_error_message
from recaptcha2.widgets import ReCaptcha2Widget


class ReCaptcha2Field(forms.CharField):
    default_error_messages = {
        'captcha_invalid': _(u'Incorrect, please try again.')
    }

    def __init__(self, public_key=None, private_key=None, use_ssl=None, item_id='captcha', explicit_render=False,
                 manual_callback=False, lang=None, *args, **kwargs):

        self.private_key = private_key if private_key else settings.RECAPTCHA_PRIVATE_KEY
        self.public_key = public_key if public_key else settings.RECAPTCHA_PUBLIC_KEY
        self.use_ssl = use_ssl if use_ssl is not None else getattr(settings, 'RECAPTCHA_USE_SSL', True)

        self.widget = ReCaptcha2Widget(public_key=self.public_key, use_ssl=self.use_ssl, item_id=item_id,
                                       explicit_render=explicit_render, manual_callback=manual_callback, lang=lang)
        self.required = True
        super(ReCaptcha2Field, self).__init__(*args, **kwargs)

    def clean(self, values):
        super(ReCaptcha2Field, self).validate(values[0])
        ret = validate_captcha(values[0], self.private_key)
        if not ret.is_clean:
            raise ValidationError(get_error_message(ret.error_code), code=ret.error_code)
        return values[0]
