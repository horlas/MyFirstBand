from django import forms
from musicians.models import UserProfile
from PIL import Image
from django.conf import settings

class ProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['username', 'bio', 'dept', 'town', 'birth_year', 'avatar']

    # def save(self):
    #     # check if the avatar has changed
    #     if 'avatar' in profile_form.changed_data:
    #         uploaded_picture = request.FILES['avatar']
    #
    #         # we rename avatar picture with the user id
    #         avatar_name = '{}.jpg'.format(request.user.id)
    #
    #         # img = Image.open(uploaded_avatar)
    #         # # convert all picture to jpg
    #         # img = img.convert('RGB')
    #         new_avatar = create_avatar_pict(uploaded_picture)
    #
    #         # the location of user_avatar
    #         location = '{}/user_avatar/'.format(settings.MEDIA_ROOT)
    #
    #         fs = FileSystemStorage(location=location)
    #         fs.save(avatar_name , new_avatar)

