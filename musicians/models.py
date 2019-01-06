from django.db import models
from djangoyearlessdate.models import YearField
from django.db.models.signals import post_save
from django.dispatch import receiver
from authentication.models import User

from django.core.files.storage import FileSystemStorage
from PIL import Image
from datetime import date
from model_utils import FieldTracker
from io import BytesIO, StringIO
from django.core.files.uploadedfile import SimpleUploadedFile, InMemoryUploadedFile
import sys
import os
from django.conf import settings

from core.utils import create_avatar_pict
# Create your models here.

fs = FileSystemStorage(location='core/media/user_avatar')

class UserProfile(models.Model):
    '''
    Custom User Profile
    '''

    GENDER_CHOICES = (
        ('H', 'Homme'),
        ('F', 'Femme'),
    )



    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=60, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    dept = models.CharField(max_length=5, blank=True)
    town = models.CharField(max_length=60, blank=True)
    birth_year = YearField(null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True, upload_to='user_avatar/')
    gender = models.CharField('gender' , max_length=1 , choices=GENDER_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
        if self.tracker.has_changed('avatar'):

            # rename avatar image
            avatar_name = '{}-{}.jpg'.format(date.today(), self.user.id)

            img = Image.open(self.avatar.path)



            # convert all picture to jpg
            img = img.convert('RGB')
            # resize picture
            img = img.resize((140 , 140) , Image.ANTIALIAS)
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

            # delete old image file
            if self.tracker.previous('avatar'):
                old_avatar = '{}{}'.format(settings.MEDIA_ROOT, self.tracker.previous('avatar'))
                os.remove(old_avatar)