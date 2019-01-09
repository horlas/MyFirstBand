from django.shortcuts import render, redirect
from .forms import ProfileForm, AvatarForm
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from core.utils import get_age


# Create your views here.
@login_required
def profile(request):
    age = get_age(request.user.userprofile.birth_year)
    datas = {
    'age' : age
    }

    return render(request, 'musicians/profile.html', datas)




@login_required
@transaction.atomic
def update_profile(request):

    if request.method == 'POST':

        avatar_form = AvatarForm(request.POST ,
                                 request.FILES ,
                                 instance=request.user.userprofile)

        profile_form = ProfileForm(request.POST,
                                   request.FILES,
                                   instance=request.user.userprofile)

        if avatar_form.is_valid() and profile_form.is_valid():
            avatar_form.save()
            profile_form.save()
            messages.success(request , _('Your profile was successfully updated!'))
            return redirect('musicians:profile')
        else:
            messages.error(request , _('Please correct the error below.'))
    #
    else:
        avatar_form = AvatarForm(instance=request.user.userprofile)
        profile_form = ProfileForm(instance=request.user.userprofile)

    return render(request , 'musicians/update_profile.html', {
        'avatar_form': avatar_form,
        'profile_form': profile_form
    })


@login_required
@transaction.atomic
def update_avatar(request):

    if request.method == 'POST':

        avatar_form = AvatarForm(request.POST,
                                 request.FILES,
                                 instance=request.user.userprofile)
        if avatar_form.is_valid():
            avatar_form.save()
            messages.success(request , _('Your profile was successfully updated!'))
            return redirect('musicians:profile')
        else:
            messages.error(request , _('Please correct the error below.'))
        #
    else:
        avatar_form= ProfileForm(instance=request.user.userprofile)

    return render(request , 'musicians/update_profile.html' , {

        'avatar_form': profile_form
    })