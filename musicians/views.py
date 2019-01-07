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

    if request.method == 'POST':

        profile_form = ProfileForm(request.POST,
                                   request.FILES,
                                   instance=request.user.userprofile)

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request , _('Your profile was successfully updated!'))
            return redirect('musicians:profile')
        else:
            messages.error(request , _('Please correct the error below.'))
    #
    else:
        profile_form = ProfileForm(instance=request.user.userprofile)

    return render(request , 'musicians/update_profile.html', {

        'profile_form': profile_form
    })


