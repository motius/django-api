import django.apps
from django.utils.translation import ugettext_lazy as _


class UserConfig(django.apps.AppConfig):
    name = 'apps.user'
    verbose_name = _('User')
