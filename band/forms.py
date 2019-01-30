from django.forms import ModelForm, Select, Form, ModelChoiceField, fields
from band.models import Band, UserBand

class ProfileBandForm(ModelForm):
    class Meta:
        model = Band
        exclude = ['owner']

        widgets = {
            'town': Select()
        }
