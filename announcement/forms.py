from django.forms import Form, ModelChoiceField, fields, ModelForm, Select, CharField
from announcement.models import MusicianAnnouncement
from django import forms

class MusicianAnnouncementForm(ModelForm):

    class Meta:
        model = MusicianAnnouncement
        exclude = ['author', 'created_at', 'is_active']



