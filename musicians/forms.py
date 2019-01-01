from django import forms
from musicians.models import UserProfile

class ProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['username', 'bio', 'dept', 'town', 'birth_year', 'avatar']