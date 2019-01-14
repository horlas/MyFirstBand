from django.db import models
from djangoyearlessdate.models import YearField
from django.db.models.signals import post_save
from django.dispatch import receiver
from authentication.models import User

from model_utils import FieldTracker
from PIL import Image
from datetime import date
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
import os
from django.conf import settings

# Create your models here.
class UserProfile(models.Model):
    '''
    Custom User Profile
    '''

    GENDER_CHOICES = (
        ('H', 'Homme'),
        ('F', 'Femme'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField("Nom", max_length=60, blank=True)
    bio = models.TextField("Courte description", max_length=500, blank=True)
    code = models.CharField("code postal", max_length=5, blank=True)
    county_name = models.CharField("Nom du département", max_length=60, blank=True)
    town = models.CharField("Ville", max_length=60, blank=True)
    birth_year = YearField("Année de naissance", null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True, upload_to='user_avatar/')
    gender = models.CharField('Genre' , max_length=1, choices=GENDER_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Here we instantiate a Fieltracker to track any fields specially avatar field
    tracker = FieldTracker()

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()


    def set_avatar(self):
        _avatar = self.avatar
        if not _avatar:
            self.avatar = 'core/media/user_avatar/0.jpg'

    def save(self, *args, **kwargs):
        super().save()

        # we get here the self avatar condition
        # in case of there is no self.avatar as example
        # after a clear action.
        if self.avatar and self.tracker.has_changed('avatar'):
            # keep the upload image path in order to delete it after
            upload_image = self.avatar.path

            # rename avatar image
            avatar_name = '{}-{}.jpg'.format(date.today(), self.user.id)

            img = Image.open(upload_image)

            # convert all picture to jpg
            img = img.convert('RGB')

            # resize picture
            img = img.resize((140, 140), Image.ANTIALIAS)

            # make readable picture
            output = BytesIO()
            img.save(output, format='JPEG', quality=100)
            output.seek(0)
            self.avatar = InMemoryUploadedFile(output,
                                              'ImageField',
                                              avatar_name,
                                              'image/jpeg',
                                              sys.getsizeof(output),
                                              None)

            super(UserProfile, self).save()

            # delete the upload of avatar before resize it
            os.remove(upload_image)

            # delete old image file
            if self.tracker.previous('avatar'):
                old_avatar = '{}{}'.format(settings.MEDIA_ROOT, self.tracker.previous('avatar'))
                os.remove(old_avatar)

        # delete old image file even in case of "clear" image action
        if not self.avatar and self.tracker.has_changed('avatar'):
            old_avatar = '{}{}'.format(settings.MEDIA_ROOT , self.tracker.previous('avatar'))
            os.remove(old_avatar)


class Instrument(models.Model):
    ''' Musicians Instruments'''

    INSTRUMENT_CHOICE = (

            ('ACCORDEON' , 'Accordéoniste'),
            ('BASSE' , 'Bassiste'),
            ('BATTERIE' , 'Batteur'),
            ('CUIVRE' , 'Cuivriste'),
            ('CLARINETTE' , 'Clarinetiste'),
            ('CLAVIER' , 'Clavieriste'),
            ('CONTREBASSE' , 'Contrebassiste'),
            ('FLUTE' , 'Flutiste'),
            ('GUITARE' , 'Guitariste'),
            ('HARMONICA' , 'Harmoniciste'),
            ('PERCUSSION' , 'Percussionniste'),
            ('PIANO' , 'Pianiste'),
            ('SAXOPHONE' , 'Saxophoniste'),
            ('VIOLON' , 'Violoniste'),
        )

    instrument = models.CharField('instrument', max_length=80, choices=INSTRUMENT_CHOICE)
    musician = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.instrument

