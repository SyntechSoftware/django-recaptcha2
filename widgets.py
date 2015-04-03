import re
from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from recaptcha2 import DEFAULT_API_SSL_SERVER, DEFAULT_API_SERVER

class ReCaptcha2Widget(forms.widgets.Widget):
    grecaptcha_response_name = 'g-recaptcha-response'

    def __init__(self, public_key=None, use_ssl=None, item_id='captcha', explicit_render=False,
                 manual_callback=False, lang=None, *args, **kwargs):
        self.public_key = public_key
        self.use_ssl = use_ssl
        self.template = getattr(settings, 'CAPTCHA_WIDGET_TEMPLATE', 'recaptcha2_widget.html')
        self.item_id = re.sub(r'[^a-zA-Z]', '', item_id)
        self.explicit_render = explicit_render
        self.manual_callback = manual_callback if explicit_render else False
        self.lang = lang if lang else settings.LANGUAGE_CODE[:2]
        super(ReCaptcha2Widget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        widget = render_to_string(self.template,
            {'api_server': DEFAULT_API_SSL_SERVER if self.use_ssl else DEFAULT_API_SERVER,
             'public_key': self.public_key,
             'lang': self.lang,
             'explicit_render': self.explicit_render,
             'manual_callback': self.manual_callback
             })

        return mark_safe(u'%s' % widget)

    def value_from_datadict(self, data, files, name):
        return [data.get(self.grecaptcha_response_name, None)]
