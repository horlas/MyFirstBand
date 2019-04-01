from django.forms import Form, ModelForm, Select, CharField
from band.models import Band


class ProfileBandForm(ModelForm):

    class Meta:
        model = Band
        exclude = ['owner', 'members', 'updated_by', 'slug']

        widgets = {
            'town': Select()
        }


class MemberCreateForm(Form):
    '''Dummy Form fot get option in Createview, this form is passed to ManageBandView'''

    band = CharField(max_length=80)
    musician = CharField(max_length=80, label="pseudo du nouveau membre")
    raison_invitation = CharField(max_length=64, label= "Raison de l'invitation" )


