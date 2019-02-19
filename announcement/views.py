from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, FormView, CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db import transaction
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.utils import timezone
# from django.views.generic import CreateView
from announcement.forms import MusicianAnnouncementForm
from announcement.models import MusicianAnnouncement
from musicians.models import Instrument

# Create your views here.


class AnnouncementCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):

    model = MusicianAnnouncement
    form_class = MusicianAnnouncementForm
    template_name = 'announcement/create_announcement.html'
    success_url = reverse_lazy('announcement:announcement_list')

    def get_initial(self):
        initial = super(AnnouncementCreateView, self).get_initial()
        initial['title'] = '{} cherche groupe'.format(
            Instrument.objects.filter(musician=self.request.user).first())
        initial['town'] = self.request.user.userprofile.town
        initial['county_name'] = self.request.user.userprofile.county_name
        return initial

    def form_valid(self, form):
        print('yes')
        form.instance.author = self.request.user
        messages.success(self.request, (" Félicitations ! Votre annonce a été créée ! "))
        return super().form_valid(form)


class AnnouncementListView(LoginRequiredMixin, ListView):
    '''this view is in charge of list the announcement writen by the request user'''

    template_name = 'announcement/announcement_list.html'
    context_object_name = 'list of announcements'

    def get_queryset(self):
        return MusicianAnnouncement.objects.filter(author=self.request.user)