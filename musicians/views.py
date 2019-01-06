from django.shortcuts import render, redirect
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _


# Create your views here.
@login_required
def profile(request):
    return render(request, 'musicians/profile.html')




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


