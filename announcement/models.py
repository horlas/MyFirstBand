from django.db import models
from authentication.models import User

# Create your models here.


class MusicianAnnouncement(models.Model):
    ''' Model to write an announcement'''

    title = models.CharField("Titre de l'annonce", max_length=80,)
    content = models.TextField("Texte de l'annonce", max_length=500)
    code = models.CharField("code postal", max_length=5, blank=True)
    county_name = models.CharField("Nom du département", max_length=60, blank=True)
    town = models.CharField("Ville", max_length=60, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class MusicianAnswerAnnouncement(models.Model):
    ''' Model to wrtite answers'''
    content = models.TextField("Reponse", max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    parent_id = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer_author')
    recipient = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='recipient_user', null=True)
    musician_announcement = models.ForeignKey(MusicianAnnouncement, on_delete=models.CASCADE)


