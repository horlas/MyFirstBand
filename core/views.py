from django.shortcuts import render, redirect
from authentication.models import User
from band.models import Band, Membership
from musicians.models import Instrument
from django.views.generic.detail import DetailView
from announcement.models import MusicianAnnouncement
from musicians.models import UserProfile
from core.utils import get_age
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests


def accueil(request):
    return render(request, 'core/index.html')


def invite_search(request):
    context = {}
    last_user = User.objects.exclude(userprofile__username='') \
                    .exclude(userprofile__avatar="").order_by('-id')[:6]
    context['last_users'] = last_user

    last_band = Band.objects.all().order_by('-id')[:6]
    context['last_bands'] = last_band
    last_announcement = MusicianAnnouncement.objects.all().order_by('-created_at')[:6]
    context['last_announcement'] = last_announcement
    return render(request, 'core/search.html', context)


def privacy(request):
    return render(request, 'core/privacy_policy.html')


def about(request):
    return render(request, 'core/about.html')


@csrf_exempt
def search(request):
    ''' ajax return of datas witch depends of an user input'''

    if request.is_ajax():
        item = request.POST.get('item')
        cp = request.POST.get('cp')
        results = []
        if item == 'Annonces' and cp == '':
            # return all announcements
            ads = MusicianAnnouncement.objects.exclude(is_active=False) \
                                      .order_by('-created_at').values('id',
                                               'title',
                                               'town',
                                               'county_name',
                                               'created_at')
            for a in ads:
                a['created_at'] = a['created_at'].strftime("%d %B %Y")
                a['tag'] = 'annonces'
                results.append(a)

        if item == 'Annonces' and cp != '':
            # query data base
            ads = MusicianAnnouncement.objects.filter(code__startswith=cp)\
                                              .exclude(is_active=False)\
                                              .order_by('-created_at').values('id',
                                                                             'title',
                                                                             'town',
                                                                             'county_name',
                                                                             'created_at')

            for a in ads:
                a['created_at'] = a['created_at'].strftime("%d %B %Y")
                a['tag'] = 'annonces'
                results.append(a)

        if item == 'Musiciens':
            # query data : users who live in the same county, and witch have some data
            mus = User.objects.filter(userprofile__code__startswith=cp)\
                                     .exclude(userprofile__username='')\
                                     .order_by('-id')

            for m in mus:
                # get instrument
                instru_queryset = m.instrument_set.all()
                dict_instru = {i.id: i.instrument for i in instru_queryset}
                # for musicians who have no avatar display default imq
                try:
                    avatar = m.userprofile.avatar.url
                except ValueError:
                    avatar = 'static/core/img/0.jpg'
                dic = {"name": m.userprofile.username, 'avatar': avatar,
                       "pk" : m.userprofile.pk, 'town': m.userprofile.town,
                       "county_name": m.userprofile.county_name,
                        "instrument" : dict_instru, "tag": "musicians"}
                results.append(dic)

        if item == 'Groupes':
            # query data : band
            bands = Band.objects.filter(code__startswith=cp) \
                                .exclude(name='') \
                                .order_by('-id')
            for b in bands:
                # for band witch have no avatar display default img
                try:
                    avatar = b.avatar.url
                except ValueError :
                    avatar = 'static/core/img/0_band.jpg'

                dic = {'name' : b.name, 'avatar' : avatar,
                       'town' : b.town, 'county_name' : b.county_name,
                       'type' : b.type, 'musical_genre' : b.musical_genre,
                       'bio' : b.bio , 'slug': b.slug, 'tag': 'groupes'}
                results.append(dic)

    else:

        results = 'fail'

    return JsonResponse(results, safe=False)


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