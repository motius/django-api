import django.apps
from django.utils.translation import ugettext_lazy as _


class FrontendConfig(django.apps.AppConfig):
    name = 'apps.frontend'
    verbose_name = _('Frontend')
