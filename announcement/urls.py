from .views import AnnouncementCreateView,AnnouncementListView
from django.urls import path

app_name = 'announcement'

urlpatterns = [

        path('list_post/', AnnouncementListView.as_view(), name='announcement_list'),
        path('create_post/', AnnouncementCreateView.as_view(), name='create_announcement')



]