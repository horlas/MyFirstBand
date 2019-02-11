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
from band.forms import ProfileBandForm, MemberCreateForm
from musicians.models import Instrument
from band.models import Membership
from musicians.models import UserProfile, User
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
        members = Membership.objects.filter(band=self.object.id)

        # data_instru ={}
        # for m in members:
        #     instru = Instrument.objects.filter(musician=m.musician).first()
        #
        #     data_instru[m.musician] = instru
        # context['instru'] = data_instru
        context['members'] = members
        context['sidenav_band'] = 'sidenav_band'

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

class ManageBandView(LoginRequiredMixin, DetailView):
    template_name = 'band/manage_band.html'
    model = Band

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        # launch membership
        members = Membership.objects.filter(band=self.object.id)
        context['members'] = members
        # launch sidenav_bar
        context['sidenav_band'] = 'sidenav_band'
        # launch add_member_form
        member_form = MemberCreateForm(self.request.GET or None)
        context['member_form'] = member_form

        return context



class AddMemberView(LoginRequiredMixin, FormView, SuccessMessageMixin):
    ''' View to add a member to a band, here is the post form.
    We create the member without Createview because we need to grab
    band name from the manage band view. We need also to add some code to
    get the musician name by an autocomplete script'''
    form_class = MemberCreateForm
    template_name = 'band/manage_band.html'

    def post(self, request, *args, **kwargs):
        member_create_form = self.form_class(request.POST)
        if member_create_form.is_valid():
            # get the band slug to redirect to manage view
            band = Band.objects.get(name=request.POST['band'])
            slug = band.slug
            # we get the User instance through Userprofile.username
            try:
                musician = User.objects.get(userprofile__username=request.POST['musician'])

            except User.DoesNotExist:
                # member_create_form = self.form_class(request.POST)
                messages.error(self.request, ("{} ne fait pas partie de MyFirstBand . ".format(request.POST['musician'])))
                return redirect(reverse_lazy('band:manage_band', kwargs={'slug': slug}))
            # get the band
            band = Band.objects.get(name=request.POST['band'],)
            # create the new member
            Membership.objects.update_or_create(band=band,
                                                musician=musician,
                                                defaults={'invite_reason':request.POST['raison_invitation']},)

            messages.success(self.request, ("{} a été ajouté au groupe ! ".format(request.POST['musician'],)))
            return redirect(reverse_lazy('band:manage_band', kwargs={'slug': slug}))

        else:
            member_create_form = self.form_class(request.POST)
            return render(
                self.get_context_data(member_form=member_create_form))


# Todo : link to each profile , must be a public profile view

def autocomplete_username(request):
    ''' Ajax view for autocomplete name of member field in add_member_form'''

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


class MembershipDelete(LoginRequiredMixin, DeleteView):

    model = Membership

    def get_success_url(self):
        referer_url = self.request.META.get('HTTP_REFERER')
        messages.success(self.request, ('{} a été supprimé!').format(self.object.musician.userprofile.username))
        return referer_url

@login_required()
def change_owner(request):
    name_new_owner = request.POST['owner_name']
    new_owner = User.objects.get(userprofile__username=name_new_owner)
    band_id = request.POST['band']
    band = Band.objects.get(id=band_id)
    band.owner = new_owner
    band.save()
    messages.success(request, '{} est le nouveau propriétaire du groupe!'.format(name_new_owner))
    slug = band.slug
    return redirect(reverse_lazy('band:manage_band', kwargs={'slug': slug}))


# Todo : views manage band
# Todo : profil public link
# Todo : error Toast
# Todo: put Js in an other directory
# Todo : delete band if the request user is owner and if there is no member any more except the owner

