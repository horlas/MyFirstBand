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


from band.forms import *
from band.models import Band, Member, MusicalGenre

# Create your views here.

class BandListView(ListView, LoginRequiredMixin):

    template_name = 'band_list.html'
    context_object_name = 'list of user bands'
    def get_queryset(self):
        return Band.objects.filter(member__member = self.request.user)



