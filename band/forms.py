from django import forms
from band.models import Band, Membership

class ProfileBandForm(forms.ModelForm):

    class Meta:
        model = Band
        exclude = ['owner', 'members', 'updated_by', 'slug']

        widgets = {
            'town': forms.Select()
        }


class MemberCreateForm(forms.Form):
    '''Dummy Form fot get option in Createview, this form is passed to ManageBandView'''

    band = forms.CharField(max_length=80)
    musician = forms.CharField(max_length=80, label="Chercher le nom du membre à ajouter")
    raison_invitation = forms.CharField(max_length=64, label= "Raison pour laquelle le musicien rejoint le groupe" )

