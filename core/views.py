from django.shortcuts import render, redirect
from authentication.models import User
from band.models import Band, Membership
from musicians.models import Instrument
from django.views.generic.detail import DetailView

from musicians.models import UserProfile

# Create your views here.


def accueil(request):
    context = {}
    last_user = User.objects.all()[:6]
    context['last_users'] = last_user
    last_band = Band.objects.all()[:6]
    context['last_bands'] = last_band

    return render(request, 'core/index.html', context)

class BandProfileView(DetailView):

    model = Band
    template_name = 'core/profile_band.html'

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
