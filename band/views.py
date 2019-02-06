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
from django.views.generic.edit import UpdateView
from django.utils import timezone
# from django.views.generic import CreateView
from band.forms import ProfileBandForm
from musicians.models import Instrument
from band.models import Membership
from musicians.models import UserProfile, User
from django.http import JsonResponse


from band.forms import *
from band.models import Band

# Create your views here.


class BandListView(LoginRequiredMixin, ListView):

    ''' this view is in charge of list the band witch member is the request user'''

    template_name = 'band_list.html'
    context_object_name = 'list of user bands'

    def get_queryset(self):

        return Band.objects.filter(members=self.request.user)


class BandCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):

    model = Band
    form_class = ProfileBandForm
    template_name = 'band/create_band.html'
    success_url = reverse_lazy('band:list_bands')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, (" Félicitations ! Votre groupe a été créé ! "))
        return super().form_valid(form)


class BandDetailView(LoginRequiredMixin, DetailView):

    model = Band

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidenav_band'] = 'sidenav_band'
        members = Membership.objects.filter(band=self.object.id)
        # data_instru ={}
        # for m in members:
        #     instru = Instrument.objects.filter(musician=m.musician).first()
        #
        #     data_instru[m.musician] = instru
        # context['instru'] = data_instru
        context['members'] = members
        # print(context['instru'])
        return context
        # Todo : add the instrument to member


class BandUpdateView(LoginRequiredMixin, UpdateView):

    model = Band
    form_class = ProfileBandForm
    template_name = 'band/edit_band.html'

    def get_context_data(self, **kwargs):
        ''' To launch sidenav band'''
        context = super().get_context_data(**kwargs)
        context['sidenav_band'] = 'sidenav_band'

        return context

    def form_valid(self, form):
        ''' to track the user who does the update for history page'''
        band = form.save(commit=False)
        band.updated_by = self.request.user
        band.updated_at = timezone.now()
        band.save()
        return redirect('band:band_detail', self.object.slug )


# ManageBandView must have forms : change owner, add and delete members and maybe delete group ...

class ManageBandView(TemplateView):
    template_name = 'band/manage_band.html'


def autocomplete_username(request):

    if request.is_ajax():
        q = request.GET.get('term', '')
        users = UserProfile.objects.filter(username__istartswith=q)
        results = []
        for user in users:
            user_json = {}
            user_json['id'] = user.id
            user_json['label'] = user.username
            user_json['value'] = user.username
            results.append(user_json)
    else:
        results = 'fail'
    return JsonResponse(results, safe=False)

# Todo : views manage band
# Todo : add members
# Todo : Change owner
# Todo : delete band if the request user is owner

