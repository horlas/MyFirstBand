from .views import *
from django.urls import path

app_name = 'announcement'

urlpatterns = [

        path('list_post/', AnnouncementListView.as_view(), name='announcement_list'),
        path('create_post/', AnnouncementCreateView.as_view(), name='create_announcement'),
        path('archive_post/<int:id>', archive_announcement, name='archive'),
        path('online_post/<int:id>', online_announcement, name='online'),
        path('update_post/<int:pk>', AnnouncementUpdateView.as_view(), name='update_announcement'),
        path('detail_post/<int:pk>', AnnouncementDetailView.as_view(), name='detail_announcement'),
        path('post_answer/submit', AnswerAnnouncement.as_view(), name='post_answer'),
        path('post_message/submit', AnswerMessage.as_view(), name='post_message'),
        path('list_message/', AnnouncementMessage.as_view(), name='announcement_messages'),
        path('ajax_calls_message/search', message_to_message, name='message_to_message'),

]