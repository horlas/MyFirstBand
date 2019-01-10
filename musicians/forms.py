from django.forms import ModelForm, Select
from musicians.models import UserProfile


class ProfileForm(ModelForm):

    class Meta:
        model = UserProfile
        fields = ['username', 'bio', 'birth_year']

class AvatarForm (ModelForm):

    class Meta:
        model = UserProfile
        fields = ['avatar']

class LocalForm (ModelForm):
    class Meta:
        model = UserProfile
        fields = ['code', 'county_name', 'town']

        widgets = {
            'town': Select
        }

