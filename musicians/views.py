from django.shortcuts import render, redirect
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from core.utils import get_age


# Create your views here.
@login_required
def profile(request):
    age = get_age(request.user.userprofile.birth_year)
    print(age)
    datas = {
    'age' : age
    }

    return render(request, 'musicians/profile.html', datas)




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


@login_required
@transaction.atomic
def update_avatar(request):

    if request.method == 'POST':

