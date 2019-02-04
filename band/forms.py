from django.forms import ModelForm, Select, Form, ModelChoiceField, fields
from band.models import Band

class ProfileBandForm(ModelForm):

    class Meta:
        model = Band
        exclude = ['owner', 'members', 'updated_by', 'slug']

        widgets = {
            'town': Select()
        }


