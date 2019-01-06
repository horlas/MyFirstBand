from django.shortcuts import render, redirect
from .forms import ProfileForm
from authentication.forms import CustomLoginForm, SignupForm
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.core.files.storage import FileSystemStorage
from core.utils import rename_file, resize_picture, create_avatar_pict
from django.views.generic.edit import UpdateView
from musicians.models import UserProfile
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from django.conf import settings

# Create your views here.
@login_required
def profile(request):
    return render(request, 'musicians/profile.html')

#
#  @login_required
#  # @transaction.atomic
# class ProfileUpdateView(UpdateView):
#     model = UserProfile
#     fields =  ['username', 'bio', 'dept', 'town', 'birth_year', 'avatar']
#     template_name = 'update_profile.html'
#     template_name_suffix = '_update_form'
#
#     def get_object(self, request):
#         user = request.user
#         return get






@login_required
@transaction.atomic
def update_profile(request):

    data = {'username': request.user.userprofile.username,
            'bio': request.user.userprofile.bio,
            'dept': request.user.userprofile.dept,
            'town': request.user.userprofile.town,
            'birth_year': request.user.userprofile.birth_year,
            'avatar' : request.user.userprofile.avatar
    }

    if request.method == 'POST':


        # user_form = SignupForm(request.POST, instance=request.user)

        profile_form = ProfileForm(request.POST,
                                   request.FILES,
                                   instance=request.user.userprofile)


        if profile_form.is_valid():
            # check if the avatar has changed
            # if 'avatar' in profile_form.changed_data:
            #     uploaded_picture = request.FILES['avatar']
            #
            #     # we rename avatar picture with the user id
            #     avatar_name = '{}.jpg'.format(request.user.id)
            #     # call the utils function create_avatar_pict
            #     new_avatar = create_avatar_pict(uploaded_picture)
            #
            #     # the location of user_avatar
            #     location = '{}'.format(settings.MEDIA_ROOT)
            #     #
            #     # fs = FileSystemStorage(location=location)
            #     # fs.save(avatar_name , new_avatar)


            # user_form.save()
            profile_form.save()
            messages.success(request , _('Your profile was successfully updated!'))
            return redirect('musicians:profile')
        else:
            messages.error(request , _('Please correct the error below.'))
    #
    else:
        # user_form = SignupForm(request.POST , instance=request.user)
        profile_form = ProfileForm(instance=request.user.userprofile)
    #
    return render(request , 'musicians/update_profile.html', {
        # 'user_form': user_form,
        'profile_form': profile_form
    })

#
# def update_profile(request):
#     return render(request, 'musicians/update_profile.html')

