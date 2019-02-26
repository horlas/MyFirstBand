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
from django.views.decorators.csrf import csrf_exempt
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
# todo: display only is active tag announcement

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

    template_name = 'announcement/answer.html'

    def post(self, request, *args, **kwargs):
        content = request.POST['answer_text']
        a_id = request.POST['a_id']
        if len(content) > 200:
            # to avoid problems with insert a response too long in database
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
            messages.success(self.request, ("Votre réponse est envoyée vous pouvez la retrouver dans Mes messages!"))
            return redirect(reverse_lazy("announcement:detail_announcement", kwargs={'pk': a_id}))


class AnnouncementMessage(LoginRequiredMixin, SuccessMessageMixin, ListView):
    '''view that displays the announcement that the user has responded to'''

    template_name = 'announcement/message.html'
    context_object_name = 'answered_ads_list'

    def get_queryset(self):
        # ads answered by request user
        object_list = MusicianAnswerAnnouncement.objects.filter(author=self.request.user)
        object_list_sorted = object_list.order_by('-musician_announcement')
        return object_list_sorted

    def get_context_data(self, *args, **kwargs):
        # ads published by request user witch have a response
        context = super(AnnouncementMessage, self).get_context_data(*args, **kwargs)
        ads = MusicianAnnouncement.objects.filter(author=self.request.user)
        # extract all the answer
        results = []
        for a in ads:
            answer = MusicianAnswerAnnouncement.objects.filter(musician_announcement=a.id)
            results.append(answer)
        # build a list witch return all data
        data = []
        for r in results:
            for a in r:
                data.append(a)
        context['response_to_published_ads'] = data
        return context







@csrf_exempt
@login_required()
def return_message(request):
    ''' ajax return of messages depends an announcement'''

    if request.is_ajax():
        q = request.POST.get('announcement')
        print(q)
        messages = MusicianAnswerAnnouncement.objects.filter(author=request.user).filter(musician_announcement=q)
        results = []
        for m in messages:
            results.append(m.content)
    else:
        results ='fail'
    return JsonResponse(results, safe=False)





# Todo : anwwer  announcement + aswer aswer announcement


