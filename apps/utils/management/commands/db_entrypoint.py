import os
import subprocess

from django.db import connections

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from django.db.utils import ConnectionDoesNotExist


class Command(BaseCommand):
    help = 'Acts as an entrypoint for the database in docker, from the app container'

    def add_arguments(self, parser):
        parser.add_argument('--database',
                            action='store',
                            dest='database',
                            default='default',
                            help='Database connection name')
        parser.add_argument('--recreate',
                            dest='recreate',
                            action='store_true')

    def handle(self, *args, **options):
        call_command('wait_for_database', database=options['database'])

        try:
            connection = connections[options['database']]
            connection.cursor()

        except ConnectionDoesNotExist:
            raise CommandError('Database "%s" does not exist in '
                               'settings' % options['database'])

        if options['recreate']:
            call_command('recreate_database')

        self.stdout.write('Running migrations')
        call_command('migrate', no_input=True)

        self.stdout.write('Loading fixtures')
        fixtures = [
            'apps/core/fixtures/initial_data.json',
            'apps/user/fixtures/user_data.json',
        ]
        call_command('loaddata', *fixtures)
