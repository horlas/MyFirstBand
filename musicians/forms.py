from django.forms import ModelForm, Select, Form, ModelChoiceField, ChoiceField, TextInput
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


class InstruCreateForm(ModelForm):

    class Meta:

        model = Instrument
        fields = ['instrument', 'level']


        # widgets = {
        #     'instrument': Select(),
        #     'level': Select()
        # }

class InstruDeleteForm(Form):

    # here we use a dummy `queryset`, because ModelChoiceField
    # requires some queryset
    instrument = ModelChoiceField(queryset=Instrument.objects.none(), empty_label=None)

    def __init__(self, user, *args, **kwargs):
        super(InstruDeleteForm, self).__init__(*args, **kwargs)
        self.fields['instrument'].queryset = Instrument.objects.filter(musician=user)
