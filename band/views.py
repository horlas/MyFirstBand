from django.shortcuts import render
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, FormView, CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.contrib import messages
from django.views.generic.list import ListView
from band.forms import ProfileBandForm


from band.forms import *
from band.models import Band, UserBand, MusicalGenre

# Create your views here.

class BandListView(ListView, LoginRequiredMixin):
    ''' this view is in charge of list the band witch member is the request user'''

    template_name = 'band_list.html'
    context_object_name = 'list of user bands'
    def get_queryset(self):
        return Band.objects.filter(userband__member=self.request.user)


class UpdateBandView(TemplateView, LoginRequiredMixin):
    ''' this view is in charge of the forms 'get' only ,
     the forms are filled with user data'''

    template_name = 'band/update_band.html'

    def get(self, request, *args, **kwargs):

        profile_form = ProfileBandForm(self.request.GET or None,
                                   )

        context = self.get_context_data(**kwargs)
        context['profile_form'] = profile_form
        return self.render_to_response(context)


class UpdateProfileBandView(FormView, SuccessMessageMixin, LoginRequiredMixin):

    form_class = ProfileBandForm
    template_name = 'band/update_band.html'

    def post(self, request, *args, **kwargs):
        profile_form = self.form_class(request.POST)
        if profile_form.is_valid():
            profile_form.save()
            # if the band has just been created with no member and no owner
            # instance the request user as the band's owner
            # instance the request user as the first band member of the band

            messages.success(self.request, (" Les données du groupe ont été mises à jour!"))
            return redirect('musicians:update_band')

        else:
            profile_form = self.form_class()
            return render(self.get_context_data(profile_form=profile_form))