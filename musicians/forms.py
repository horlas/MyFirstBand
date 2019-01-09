from django import forms
from musicians.models import UserProfile
from PIL import Image
from django.conf import settings

class ProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['username', 'bio', 'birth_year']

class AvatarForm (forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['avatar']

class LocalForm (forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['dept', 'town']
