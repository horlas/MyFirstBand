from django.forms import ModelForm, Select, Form, ModelChoiceField, fields
from band.models import Band, UserBand, MusicalGenre

class ProfileBandForm(ModelForm):
    class Meta:
        model = Band
        fields = ['name', 'bio', 'type']
