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
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
# from django.views.generic import CreateView
from announcement.forms import MusicianAnnouncementForm
from announcement.models import MusicianAnnouncement, MusicianAnswerAnnouncement
from musicians.models import Instrument
from authentication.models import User

# Create your views here.


class AnnouncementCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    # todo :article for pythonclassmates get initial data in a form

    model = MusicianAnnouncement
    form_class = MusicianAnnouncementForm
    template_name = 'announcement/create_announcement.html'
    success_url = reverse_lazy('announcement:announcement_list')

    def get_initial(self):
        initial = super(AnnouncementCreateView, self).get_initial()
        initial['title'] = '{} cherche groupe'.format(
            Instrument.objects.filter(musician=self.request.user).first())
        return initial

    def form_valid(self, form):
        form.instance.author = self.request.user
        # by default we get request user localisation datas
        if not form.instance.code:
            form.instance.code = self.request.user.userprofile.code
            form.instance.county_name = self.request.user.userprofile.county_name
            form.instance.town = self.request.user.userprofile.town
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
    ''' View record the response to an announcement so here is the first message'''
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
            # the request_user can not answer to his own announcement
            if a.author == self.request.user:
                messages.error(self.request, 'Vous ne pouvez pas répondre à votre propre annonce')
                return redirect(reverse_lazy("announcement:detail_announcement", kwargs={'pk': a_id}))
            else:
                response = MusicianAnswerAnnouncement(
                    content = content,
                    created_at=timezone.now(),
                    author=self.request.user,
                    musician_announcement=a,
                    recipient=a.author
                     )
                response.save()
                # todo : we can imagine here send an email to the recipient
                # print(a.author) # email of the recipient
                messages.success(self.request, ("Votre réponse est envoyée vous pouvez la retrouver dans Mes messages!"))
                return redirect(reverse_lazy("announcement:detail_announcement", kwargs={'pk': a_id}))


class AnswerMessage(LoginRequiredMixin, SuccessMessageMixin, FormView):
    ''' View witch records the answer to a message'''

    template_name = 'announcement/message.html'

    def post(self, request, *args, **kwargs):
        content = request.POST['message_text']
        parent_id = request.POST['m_id']
        parent_ads = request.POST['m_ads']
        parent_recipient = request.POST['m_recipient']
        if len(content) > 200:
            # to avoid problems with insert a response too long in database
            messages.error(self.request, 'Réponse trop longue')
            return redirect(reverse_lazy("announcement:announcement_messages"))
        else:
            a = MusicianAnnouncement.objects.get(id=parent_ads)
            init_message = MusicianAnswerAnnouncement.objects.get(id=parent_id)
            user_recipient = User.objects.get(userprofile__username=parent_recipient)
            response = MusicianAnswerAnnouncement(
                content=content,
                created_at=timezone.now(),
                author=self.request.user,
                parent_id=init_message,
                musician_announcement=a,
                recipient=user_recipient,
            )
            response.save()

            # todo : we can here imagine send an email to the recipient
            # print(user_recipient)
            messages.success(self.request, ("Votre réponse est postée"))
        return redirect(reverse_lazy("announcement:announcement_messages"))


class AnnouncementMessage(LoginRequiredMixin, SuccessMessageMixin, ListView):
    '''view that displays the announcement that the user has responded to and the first messages to his ads'''

    template_name = 'announcement/message.html'
    context_object_name = 'answered_ads_list'

    def get_queryset(self):
        # ads answered by request user
        object_list = MusicianAnswerAnnouncement.objects.filter(author=self.request.user)\
                                                        .filter(parent_id__isnull=True) \
                                                        .order_by('created_at')

        return object_list

    def get_context_data(self, *args, **kwargs):
        # ads published by request user witch have a response
        context = super(AnnouncementMessage, self).get_context_data(*args, **kwargs)
        ads = MusicianAnnouncement.objects.filter(author=self.request.user).values('id')
        # extract all the answer
        results = []
        for a in ads:
            answer = MusicianAnswerAnnouncement.objects.filter(musician_announcement=a['id']).filter(parent_id__isnull=True)
            results.append(answer)
        # build a list witch return all data because here we have context datas not queryset
        data = []
        for r in results:
            for a in r:
                data.append(a)
        context['response_to_published_ads'] = data
        return context


@csrf_exempt
@login_required()
def message_to_message(request):
    ''' ajax return of messages witch depends of a parent_id'''

    if request.is_ajax():
        q = request.POST.get('parent_message')
        print(q)
        messages = MusicianAnswerAnnouncement.objects.filter(parent_id=q).order_by('created_at')
        results = []
        for m in messages:
            date= m.created_at.strftime("%d %B %Y")
            # todo : display date of message
            dic = {"content": m.content, "author": m.author.userprofile.username, "created_at": date, "author_userprofile_id" : m.author.userprofile.pk }
            results.append(dic)
    else:
        results ='fail'
    return JsonResponse(results, safe=False)



