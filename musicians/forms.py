from django.forms import ModelForm, Select, ModelChoiceField, ChoiceField, TextInput
from musicians.models import UserProfile, Instrument


class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'bio', 'birth_year', 'gender']


class AvatarForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']


class LocalForm(ModelForm):
    class Meta:
        # town = (
        #     ('1' , 'Montpellier') ,
        #     ('2' , 'Nimes') ,
        #     ('3' , 'Beziers') ,
        # )

        model = UserProfile
        fields = ['code', 'county_name', 'town']

        widgets = {
            'town': Select()  # choices=town
        }


class InstruForm(ModelForm):


    class Meta:

        model = Instrument
        fields = ['instrument']

        widgets = {
            'instrument': Select()
        }
