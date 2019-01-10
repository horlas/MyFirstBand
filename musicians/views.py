from django.shortcuts import render, redirect
from .forms import ProfileForm, AvatarForm, LocalForm
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from core.utils import get_age


# Create your views here.
@login_required
def profile(request):
    if request.user.userprofile.birth_year:
        age = get_age(request.user.userprofile.birth_year)
        datas = {
            'age' : age
            }

        return render(request, 'musicians/profile.html', datas)
    else:
        return render(request, 'musicians/profile.html')




@login_required
@transaction.atomic
def update_profile(request):

    if request.method == 'POST':

        avatar_form = AvatarForm(request.POST ,
                                 request.FILES ,
                                 instance=request.user.userprofile)

        profile_form = ProfileForm(request.POST,
                                   instance=request.user.userprofile)

        local_form = LocalForm(request.POST ,
                               instance=request.user.userprofile)

        print(request.POST.get("town"))
        if avatar_form.is_valid() and profile_form.is_valid() and local_form.is_valid():

            avatar_form.save()
            profile_form.save()
            local_form.save()

            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('musicians:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    #
    else:
        avatar_form = AvatarForm(instance=request.user.userprofile)
        profile_form = ProfileForm(instance=request.user.userprofile)
        local_form = LocalForm(instance=request.user.userprofile)

    return render(request , 'musicians/update_profile.html', {
        'avatar_form': avatar_form,
        'profile_form': profile_form,
        'local_form' : local_form

    })






#
# @login_required
# @transaction.atomic
# def update_location(request):
#     datas = {
#         'age': 'HOUOUOU'
#     }
#
#     if request.method == 'POST':
#
#
#         if local_form.is_valid():
#             local_form.save()
#             messages.success(request , _('Your profile was successfully updated!'))
#             return redirect('musicians:profile')
#         else:
#             messages.error(request , _('Please correct the error below.'))
#
#     else:
#         local_form = LocalForm(instance=request.user.userprofile)
#
#     return render(request, 'musicians/update_profile.html', {
#         "local_form": local_form,
#         "age" : age
#     })