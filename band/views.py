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
from django.views.generic.detail import DetailView
# from django.views.generic import CreateView
from band.forms import ProfileBandForm
from band.models import Membership


from band.forms import *
from band.models import Band

# Create your views here.

class BandListView(ListView, LoginRequiredMixin):
    ''' this view is in charge of list the band witch member is the request user'''

    template_name = 'band_list.html'
    context_object_name = 'list of user bands'
    def get_queryset(self):
        return Band.objects.filter(members=self.request.user)




class BandCreateView(CreateView, SuccessMessageMixin, LoginRequiredMixin):

    model = Band
    form_class = ProfileBandForm
    template_name = 'band/update_band.html'
    success_url = reverse_lazy('band:list_bands')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, (" Félicitations ! Votre groupe a été créé ! "))
        return super().form_valid(form)


class BandDetailView(DetailView, LoginRequiredMixin):

    model = Band

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidenav_band'] = 'sidenav_band'
        return context



# Todo : Update Band View
# Todo : Detailview
# Todo : SidenavBand
# Todo : add members
# Todo : Change owner
# Todo : delete band if the request user is owner

