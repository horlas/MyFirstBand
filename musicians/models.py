from django.db import models
from djangoyearlessdate.models import YearField
from django.db.models.signals import post_save
from django.dispatch import receiver
from authentication.models import User

# Create your models here.



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=60, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    dept = models.CharField(max_length=5, blank=True)
    town = models.CharField(max_length=60, blank=True)
    birth_year = YearField(null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True, upload_to='./media/user_avatar/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()