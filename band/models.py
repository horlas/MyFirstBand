from django.db import models
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
from django.utils.text import slugify

# Create your models here.


class Band(models.Model):
    ''' Model to manage band '''

    COM = "Groupe de Compos"
    REP = 'Groupe de Reprises'

    TYPE_OF_BAND = (

        ( COM , 'Groupe de Compos'),
        ( REP , 'Groupe de Reprises'),
    )

    BLU = 'Blues'
    CHO = 'Chorale'
    ELE = 'Electro'
    FOL = 'Folk'
    FUN = 'Funk'
    JAZ = 'Jazz'
    MET = 'Metal'
    MUS = 'Musique du Monde'
    POP = 'Pop'
    PUN = 'Punk'
    RAP = 'Rap'
    REG = 'Reggae'
    ROC = "Rock 'n' roll"
    SKA = 'Ska'
    SOU = 'Soul'
    VAR = 'Variété'

    MUSICAL_GENRE_CHOICE = (
        (BLU, 'Blues'),
        (CHO, 'Chorale'),
        (ELE, 'Electro'),
        (FOL, 'Folk'),
        (FUN, 'Funk'),
        (JAZ, 'Jazz'),
        (MET, 'Metal'),
        (MUS, 'Musique du Monde'),
        (POP, 'Pop'),
        (PUN, 'Punk'),
        (RAP, 'Rap'),
        (REG, 'Reggae'),
        (ROC, "Rock 'n' roll"),
        (SKA, 'Ska'),
        (SOU, 'Soul'),
        (VAR, 'Variété'),
    )

    BLU = 'Blues'
    CHO = 'Chorale'
    ELE = 'Electro'
    FOL = 'Folk'
    FUN = 'Funk'
    JAZ = 'Jazz'
    MET = 'Metal'
    MUS = 'Musique du Monde'
    POP = 'Pop'
    PUN = 'Punk'
    RAP = 'Rap'
    REG = 'Reggae'
    ROC = "Rock 'n' roll"
    SKA = 'Ska'
    SOU = 'Soul'
    VAR = 'Variété'

    MUSICAL_GENRE_CHOICE = (
        (BLU, 'Blues'),
        (CHO, 'Chorale'),
        (ELE, 'Electro'),
        (FOL, 'Folk'),
        (FUN, 'Funk'),
        (JAZ, 'Jazz'),
        (MET, 'Metal'),
        (MUS, 'Musique du Monde'),
        (POP, 'Pop'),
        (PUN, 'Punk'),
        (RAP, 'Rap'),
        (REG, 'Reggae'),
        (ROC, "Rock 'n' roll"),
        (SKA, 'Ska'),
        (SOU, 'Soul'),
        (VAR, 'Variété'),
    )


    name = models.CharField('Nom du Groupe',
                            max_length=80,
                            default='En cours de création',
                            unique=True,

                            )

    bio = models.TextField("Description du groupe",
                           max_length=500,
                           blank=True)

    code = models.CharField("code postal", max_length=5, blank=True)
    county_name = models.CharField("Nom du département", max_length=60, blank=True)
    town = models.CharField("Ville", max_length=60, blank=True)
    avatar = models.ImageField(null=True, blank=True, upload_to='band_avatar/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    type = models.CharField('Type de groupe', max_length=80, choices=TYPE_OF_BAND, blank=True, null=True)
    musical_genre = models.CharField('Genre musical', max_length=80, choices=MUSICAL_GENRE_CHOICE, blank=True, null=True )
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name='owner_band')
    members = models.ManyToManyField(User, through='Membership')
    slug = models.SlugField(max_length=150,  null=True)
    updated_by = models.ForeignKey(User, null= True, blank= True, on_delete=models.DO_NOTHING, related_name='update')


    # Here we instantiate a Fieltracker to track any fields specially avatar field
    tracker = FieldTracker()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.name)
            super(Band, self).save()
        if self.tracker.has_changed('name'):
            self.slug = slugify(self.name)
            super(Band, self).save()




        # we get here the self avatar condition
        # in case of there is no self.avatar as example
        # after a clear action.
        if self.avatar and self.tracker.has_changed('avatar'):
            # keep the upload image path in order to delete it after
            upload_image = self.avatar.path

            # rename avatar image
            avatar_name = '{}-{}.jpg'.format(date.today(), self.id)

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

            super(Band, self).save()

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


class Membership(models.Model):

    musician = models.ForeignKey(User, on_delete=models.CASCADE)
    band = models.ForeignKey(Band, on_delete=models.CASCADE)
    date_joined = models.DateField(auto_now_add=True)
    invite_reason = models.CharField(max_length=64)

    @receiver(post_save, sender=Band)
    def create_first_member(sender, instance, created, **kwargs):
        if created:
            first_member = Membership(musician = instance.owner,
                                      band = instance,
                                      invite_reason = "band's fouder")
            first_member.save()



