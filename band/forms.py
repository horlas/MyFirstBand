from django.forms import Form, ModelChoiceField, fields, ModelForm, Select, CharField
from band.models import Band, Membership
from django import forms

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
    musician = CharField(max_length=80, label="Chercher le nom du membre à ajouter")
    raison_invitation = CharField(max_length=64, label= "Raison pour laquelle le musicien rejoint le groupe" )


class ChangeOwnerForm(Form):
    ''' Form to send a queryset among the members of the band to choose owner of the band'''

    # here we use a dummy `queryset`, because ModelChoiceField
    # requires some queryset
    membre = ModelChoiceField(queryset=Membership.objects.none(), empty_label=None)
    # choice = (('1', 'First',), ('2', 'Second',))
    # member = forms.ChoiceField(widget=forms.RadioSelect, choices=choice)

    def __init__(self, band_id, *args, **kwargs):
        super(ChangeOwnerForm, self).__init__(*args, **kwargs)
        print('{} youyou'.format(band_id))
        self.fields['membre'].queryset = Membership.objects.filter(band=band_id)


