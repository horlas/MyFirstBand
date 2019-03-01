import os
from django.core.management import call_command
from django.core.management.base import BaseCommand
import sys
from io import StringIO



class Command(BaseCommand):
    ''' create dump authentication.Users and the rest of database'''
    buf = StringIO()

    def handle(self, *args, **options):

        call_command('dumpdata', 'authentication',  indent=4, stdout=self.buf)

        self.buf.seek(0)
        with open('core/fixtures/user-data.json', 'w') as f:
            f.write(self.buf.read())

        # test the fixture is well created
        content = os.path.getsize('core/fixtures/user-data.json')
        if content != 0:
            self.stdout.write(
                self.style.SUCCESS('Successfully created fixtures for the users '))
        else:
            self.stdout.write(self.style.WARNING('Le fichier de fixture est vide'))

        call_command('dumpdata', 'musicians', 'band', 'announcement',  indent=4, stdout=self.buf)
        self.buf.seek(0)
        with open('core/fixtures/data.json', 'w') as f:
            f.write(self.buf.read())

        # test the fixture is well created
        content = os.path.getsize('core/fixtures/data.json')
        if content != 0:
            self.stdout.write(
                self.style.SUCCESS('Successfully created fixtures for the rest of the web site '))
        else:
            self.stdout.write(self.style.WARNING('Le fichier de fixture est vide'))