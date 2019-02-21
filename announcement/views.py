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
from announcement.models import MusicianAnnouncement, MusicianAnswerAnnouncement
from musicians.models import Instrument
from authentication.models import User

# Create your views here.


class AnnouncementCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    # todo :article for pythonclassmates

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
        form.instance.author = self.request.user
        messages.success(self.request, (" Félicitations ! Votre annonce a été créée ! "))
        return super().form_valid(form)


class AnnouncementListView(LoginRequiredMixin, ListView):
    '''this view is in charge of list the announcement writen by the request user'''

    template_name = 'announcement/announcement_list.html'
    context_object_name = 'list of announcements'

    def get_queryset(self):
        return MusicianAnnouncement.objects.filter(author=self.request.user)

@login_required()
def archive_announcement(request, *args, **kwargs):
    signal = request.POST['signal']
    announcement = MusicianAnnouncement.objects.get(id=signal)
    announcement.is_active = False
    announcement.save()
    messages.success(request, "L'annonce a été archivée")
    return redirect(reverse_lazy('announcement:announcement_list'))

@login_required()
def online_announcement(request, *args, **kwargs):
    signal = request.POST['signal2']
    announcement = MusicianAnnouncement.objects.get(id=signal)
    announcement.is_active = True
    announcement.save()
    messages.success(request, "L'annonce a été mise en ligne")
    return redirect(reverse_lazy('announcement:announcement_list'))


class AnnouncementUpdateView(LoginRequiredMixin, UpdateView, SuccessMessageMixin):
    ''' to update an announcement'''

    model = MusicianAnnouncement
    form_class = MusicianAnnouncementForm
    template_name = 'announcement/update_announcement.html'

    def form_valid(self, form):
        ''' to update the announcement's date'''
        annonce = form.save(commit=False)
        annonce.created_at = timezone.now()
        annonce.save()
        messages.success(self.request, " Votre annonce a été mise à jour ! " )
        return redirect(reverse_lazy('announcement:announcement_list'))


class AnnouncementDetailView(DetailView):

    model = MusicianAnnouncement
    template_name = 'announcement/announcement.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # return elements for to display profile author link
        author = User.objects.get(id=self.object.author.id)
        context['author'] = author
        return context


class AnswerAnnouncement(LoginRequiredMixin, SuccessMessageMixin, FormView):

    template_name = 'announcement/announcement.html'

    def post(self, request, *args, **kwargs):
        content = request.POST['answer_text']
        a_id = request.POST['a_id']
        if len(content) > 200:
            messages.error(self.request, 'Réponse trop longue')
            return redirect(reverse_lazy("announcement:detail_announcement", kwargs={'pk': a_id}))
        else:
            # get the announcement to link the answer
            a = MusicianAnnouncement.objects.get(id=a_id)
            response = MusicianAnswerAnnouncement(
                content = content,
                created_at=timezone.now(),
                author=self.request.user,
                musician_announcement=a
            )
            response.save()
            messages.success(self.request, ("Votre réponse est envoyée vous pouvez la retrouver dans Mes annonces!"))
            return redirect(reverse_lazy("announcement:detail_announcement", kwargs={'pk': a_id}))




# Todo : anwwer  announcement + aswer aswer announcement

