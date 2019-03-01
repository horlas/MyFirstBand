from django.core.management.base import BaseCommand
from authentication.models import User
from musicians.models import UserProfile, Instrument
from band.models import Band, Membership
from announcement.models import MusicianAnnouncement, MusicianAnswerAnnouncement

class Command(BaseCommand):

    help = 'Delete a specificate database table'

    def add_arguments(self, parser):

        # Named (optional) arguments
        parser.add_argument(
            '--delete',
            action='store_true',
            dest='delete',
            help='Delete all table',
        )

    def handle(self, *args, **options):


        table_1 = Membership.objects.all()
        table_3 = Instrument.objects.all()
        table_2 = Band.objects.all()
        table_4 = UserProfile.objects.all()
        table_5 = User.objects.all()
        table_6 = MusicianAnswerAnnouncement.objects.all()
        table_7 = MusicianAnnouncement.objects.all()



        if options['delete']:
            table_6.delete()
            self.stdout.write(self.style.SUCCESS('Successfully deleted  MusicianAnswerAnnouncement table '))
            table_7.delete()
            self.stdout.write(self.style.SUCCESS('Successfully deleted  MusicianAnnouncement table '))
            table_1.delete()
            self.stdout.write(self.style.SUCCESS('Successfully deleted  Membership table '))
            table_2.delete()
            self.stdout.write(self.style.SUCCESS('Successfully deleted  Instrument table '))
            table_3.delete()
            self.stdout.write(self.style.SUCCESS('Successfully deleted  Band table '))
            table_4.delete()
            self.stdout.write(self.style.SUCCESS('Successfully deleted  UserProfile table '))
            table_5.delete()
            self.stdout.write(self.style.SUCCESS('Successfully deleted  User table '))
