from django.shortcuts import render, redirect
from authentication.models import User
from band.models import Band, Membership
from musicians.models import Instrument
from django.views.generic.detail import DetailView
from announcement.models import MusicianAnnouncement
from musicians.models import UserProfile
from core.utils import get_age
from django.contrib.auth.decorators import login_required
import os

# Create your views here.


def accueil(request):
    context = {}
    last_user = User.objects.all().order_by('-id')[:6]
    # Todo : when user sign up , we don't need to display an empty profil
    context['last_users'] = last_user

    last_band = Band.objects.all().order_by('-id')[:6]
    context['last_bands'] = last_band
    last_announcement = MusicianAnnouncement.objects.all().order_by('-created_at')[:6]
    context['last_announcement'] = last_announcement

    return render(request, 'core/index.html', context)


def privacy(request):
    return render(request, 'core/privacy_policy.html')


class BandProfileView(DetailView):

    model = Band
    template_name = 'core/profile_public_band.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        members = Membership.objects.filter(band=self.object.id)

        data_instru ={}
        for m in members:
            instru = Instrument.objects.filter(musician=m.musician).first()

            data_instru[m.musician] = instru
        context['instru'] = data_instru
        context['members'] = members
        return context
        # Todo : add the instrument to member


class MusicianProfileView(DetailView):

    model = UserProfile
    template_name = 'core/profile_public_musician.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        # return elements for band displaying
        bands = Band.objects.filter(members=self.object.user.id)

        context['bands'] = bands
        # return element for intsrument displaying because
        # Instrument table has no link with userprofile
        instruments = Instrument.objects.filter(musician=self.object.user.id)
        context['instruments'] = instruments
        if self.object.birth_year:
            # return musician age
            age = get_age(self.object.birth_year)
            age_str = '{} ans'.format(age)
            context['age'] = age_str

        return context