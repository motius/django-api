import django.apps
from django.utils.translation import ugettext_lazy as _


class UtilsConfig(django.apps.AppConfig):
    name = 'apps.utils'
    verbose_name = _('Utilities')
