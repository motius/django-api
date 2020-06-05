import json
import os
from io import StringIO

from django.apps.registry import apps
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.test.client import RequestFactory
from django.contrib.auth import get_user_model

from rest_framework_swagger.views import get_swagger_view


class Command(BaseCommand):
    help = 'Exports the OpenAPI spec to a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str)

    def handle(self, *args, **options):
        with open(options['path'], 'w') as f:
            request = RequestFactory().get('/api/docs/?format=openapi')
            request.user = get_user_model()(is_superuser=True)  # So OpenAPI thinks we're logged in
            spec = json.loads(get_swagger_view()(request=request).render().content)
            f.write(json.dumps(spec, indent=2))
        self.stdout.write('Wrote to {}'.format(options['path']))
