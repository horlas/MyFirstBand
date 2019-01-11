from django.shortcuts import render, redirect
from .forms import ProfileForm, AvatarForm, LocalForm
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateResponseMixin
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




# @login_required
# @transaction.atomic
# def update_profile(request):
#
#     if request.method == 'POST':
#
#         avatar_form = AvatarForm(request.POST ,
#                                  request.FILES ,
#                                  instance=request.user.userprofile)
#
#         profile_form = ProfileForm(request.POST,
#                                    instance=request.user.userprofile)
#
#         local_form = LocalForm(request.POST ,
#                                instance=request.user.userprofile)
#
#         print(request.POST.get("town"))
#         if avatar_form.is_valid() and profile_form.is_valid() and local_form.is_valid():
#             avatar_form.save()
#             profile_form.save()
#             local_form.save()
#
#             messages.success(request, _('Your profile was successfully updated!'))
#             return redirect('musicians:profile')
#         else:
#             messages.error(request, _('Please correct the error below.'))
#     #
#     else:
#         avatar_form = AvatarForm(instance=request.user.userprofile)
#         profile_form = ProfileForm(instance=request.user.userprofile)
#         local_form = LocalForm(instance=request.user.userprofile)
#
#     return render(request , 'musicians/update_profile.html', {
#         'avatar_form': avatar_form,
#         'profile_form': profile_form,
#         'local_form' : local_form,
#
#     })
#

#
class UpdateProfilView(TemplateView):

    template_name = 'musicians/update_profile.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        avatar_form = AvatarForm(self.request.GET or None,
                                 instance=request.user.userprofile)
        profile_form = ProfileForm(self.request.GET or None,
                                   instance=request.user.userprofile)
        local_form = LocalForm(self.request.GET or None,
                               instance=request.user.userprofile)
        context = self.get_context_data(**kwargs)
        context['avatar_form'] = avatar_form
        context['profile_form'] = profile_form
        context['local_form'] = local_form
        return self.render_to_response(context)


class UpdateAvatarView(FormView, SuccessMessageMixin):

    form_class = AvatarForm
    template_name = 'musicians/update_profile.html'
    success_url = '/'
    sucess_message  = "Votre image a été correctement mise à jour!"

    @method_decorator(login_required)
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        avatar_form = self.form_class(request.POST,
                                      request.FILES ,
                                      instance=request.user.userprofile)
        # profile_form = ProfileForm(request.POST ,
        #                             instance=request.user.userprofile)
        # local_form = LocalForm(request.POST ,
        #                          instance=request.user.userprofile))
        if avatar_form.is_valid():
            avatar_form.save()
            # return self.render_to_response(
            #     self.get_context_data(sucess=True))
            return redirect('musicians:update_profile') #, self.get_context_data(success=True))

        else:
            avatar_form = self.form_class(instance=request.user.userprofile)

            return self.render_to_response(
               self.get_context_data(avatar_form =avatar_form))


class UpdateDataView(FormView , SuccessMessageMixin):

    form_class = ProfileForm
    template_name = 'musicians/update_profile.html'
    success_url = 'update_profile/'
    sucess_message = "Vos données ont été correctement mise à jour!"

    @method_decorator(login_required)
    @transaction.atomic
    def post(self , request , *args , **kwargs):
        profile_form = self.form_class(request.POST ,
                                       instance=request.user.userprofile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('musicians:update_profile')

        else:
            profile_form = self.form_class(instance=request.user.userprofile)

            return self.render_to_response(
                self.get_context_data(profile_form=profile_form))



class UpdateLocalView(FormView , SuccessMessageMixin):
    form_class = LocalForm
    template_name = 'musicians/update_profile.html'
    success_url = '/'
    sucess_message = "Vos données ont été correctement mise à jour!"

    @method_decorator(login_required)
    @transaction.atomic
    def post(self , request , *args , **kwargs):
        local_form = self.form_class(request.POST ,
                                       instance=request.user.userprofile)
        if local_form.is_valid():
            local_form.save()
            return redirect('musicians:update_profile')

        else:
            local_form = self.form_class(instance=request.user.userprofile)

            return self.render_to_response(
                self.get_context_data(local_form=local_form))





















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