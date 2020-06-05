import logging
from io import StringIO
from subprocess import CalledProcessError, check_output

from django.apps import apps
from django.core.management import call_command
from django.test import TestCase
from django.test.utils import override_settings
from django.urls import reverse

log = logging.getLogger(__name__)


class TestLicenses(TestCase):
    def test_licenses(self):
        try:
            output = check_output(["liccheck", "-s", "license-strategy.ini", "-r", "requirements-devel.txt"])
            returncode = 0
        except CalledProcessError as e:
            output = e.output
            returncode = e.returncode
            print(output.decode())
        self.assertEqual(returncode, 0, 'License checker found requirements that are not vaild according to license-strategy.ini')
