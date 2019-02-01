from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, FormView, CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.contrib import messages

from core.utils import get_age
from musicians.forms import ProfileForm, AvatarForm, LocalForm, InstruDeleteForm, InstruCreateForm
from musicians.models import Instrument


# Create your views here.
@login_required
def profile(request):
    if request.user.userprofile.birth_year:
        age = get_age(request.user.userprofile.birth_year)
        age_str = '{} ans'.format(age)
        datas = {
            'age' : age_str
            }

        return render(request, 'musicians/profile.html', datas)
    else:
        return render(request, 'musicians/profile.html')


class UpdateProfilView(TemplateView):

    template_name = 'musicians/update_profile.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        avatar_form = AvatarForm(self.request.GET or None,
                                 instance=request.user.userprofile)
        profile_form = ProfileForm(self.request.GET or None,
                                   instance=request.user.userprofile)
        instru_form = InstruCreateForm(self.request.GET or None)
        del_instru_form = InstruDeleteForm(request.user)
        local_form = LocalForm(self.request.GET or None,
                               instance=request.user.userprofile)
        context = self.get_context_data(**kwargs)
        context['avatar_form'] = avatar_form
        context['profile_form'] = profile_form
        context['local_form'] = local_form
        context['instru_form'] = instru_form
        context['del_instru_form'] = del_instru_form
        return self.render_to_response(context)


class UpdateAvatarView(FormView, SuccessMessageMixin):

    form_class = AvatarForm
    template_name = 'musicians/update_profile.html'

    @method_decorator(login_required)
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        avatar_form = self.form_class(request.POST,
                                      request.FILES ,
                                      instance=request.user.userprofile)

        if avatar_form.is_valid():
            avatar_form.save()
            messages.success(self.request, (" Votre image a été  mise à jour!"))
            return redirect('musicians:update_profile') #, self.get_context_data(success=True))

        else:
            avatar_form = self.form_class(instance=request.user.userprofile)

            return self.render_to_response(
               self.get_context_data(avatar_form =avatar_form))


class UpdateDataView(FormView, SuccessMessageMixin):

    form_class = ProfileForm
    template_name = 'musicians/update_profile.html'

    @method_decorator(login_required)
    @transaction.atomic
    def post(self , request , *args , **kwargs):
        profile_form = self.form_class(request.POST,
                                       instance=request.user.userprofile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(self.request , (" Vos données ont été mises à jour!"))
            return redirect('musicians:update_profile')

        else:
            profile_form = self.form_class(instance=request.user.userprofile)

            return render(
                self.get_context_data(profile_form=profile_form))


# Todo : errors forms are  not  displayed


class UpdateLocalView(FormView, SuccessMessageMixin):

    form_class = LocalForm
    template_name = 'musicians/update_profile.html'

    @method_decorator(login_required)
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        local_form = self.form_class(request.POST,
                                       instance=request.user.userprofile)
        if local_form.is_valid():

            local_form.save()
            messages.success(self.request, (" Votre localité a été mise à jour!"))
            return redirect('musicians:update_profile')

        else:
            local_form = self.form_class(instance=request.user.userprofile)

            return render(self.get_context_data(local_form=local_form))


class InstruCreateView(LoginRequiredMixin, CreateView, SuccessMessageMixin):
    '''View to add instrument to a musician'''

    model = Instrument
    fields = ['instrument', 'level']
    template_name = 'musicians/update_profile.html'
    success_url = reverse_lazy('musicians:update_profile')

    def form_valid(self, instru_form):
        instru_form.instance.musician = self.request.user
        messages.success(self.request, ("Votre Instrument a été ajouté ! "))
        return super().form_valid(instru_form)


class InstruDeleteView(FormView, SuccessMessageMixin):
    '''View to delete instrument based on a Formwview because with deleteview
    we can not have the select option. So we use a custom form
    witch display a queryset : request. user instrument'''

    template_name = 'musicians/update_profile.html'
    success_url = reverse_lazy('musicians:update_profile')

    @method_decorator(login_required)
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        del_instru_form = InstruDeleteForm(request.user, request.POST)
        # get instrument id user wants to delete
        delete_id = request.POST['instrument']
        if del_instru_form.is_valid():
            delete_instrument = Instrument.objects.get(id=delete_id)
            delete_instrument.delete()
            messages.success(self.request, ("Votre Instrument a été supprimé ! "))
            return redirect(self.success_url)










