from django.forms import Form, ModelChoiceField, fields, ModelForm, Select, CharField
from announcement.models import MusicianAnnouncement
from django import forms

class MusicianAnnouncementForm(ModelForm):

    class Meta:
        model = MusicianAnnouncement
        exclude = ['author', 'created_at', 'is_active']

# class AnswerForm(ModelForm):
#     ''' dumy form to display on get view : announcement detail view'''
#
#     content = CharField(max_length=200, label="Votre réponse")
#

