from django.test import TestCase
from django_admin_smoke_tests.tests import AdminSiteSmokeTestMixin


class AdminSiteSmokeTest(AdminSiteSmokeTestMixin, TestCase):
    fixtures = []

    def setUp(self):
        super().setUp()
