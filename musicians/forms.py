from django.forms import ModelForm, Select, Form, ModelChoiceField, fields
from musicians.models import UserProfile, Instrument
from core.utils import current_year


class ProfileForm(ModelForm):
    birth_year = fields.IntegerField(min_value=1918, max_value=current_year())

    class Meta:
        model = UserProfile
        fields = ['username', 'bio', 'birth_year', 'gender']


class AvatarForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']


class LocalForm(ModelForm):
    class Meta:

        model = UserProfile
        fields = ['code', 'county_name', 'town']

        widgets = {
            'town': Select()
        }


class InstruCreateForm(ModelForm):
    '''Dummy Form fot get option in Createview, this form is passed to UpdateProfilView'''
    class Meta:

        model = Instrument
        fields = ['instrument', 'level']


class InstruDeleteForm(Form):

    # here we use a dummy `queryset`, because ModelChoiceField
    # requires some queryset
    instrument = ModelChoiceField(queryset=Instrument.objects.none(), empty_label=None)

    def __init__(self, user, *args, **kwargs):
        super(InstruDeleteForm, self).__init__(*args, **kwargs)
        self.fields['instrument'].queryset = Instrument.objects.filter(musician=user)
