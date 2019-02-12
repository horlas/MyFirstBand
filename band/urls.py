from band.views import *
from django.urls import path
from django.conf.urls import url

app_name = 'band'

urlpatterns = [

    path('listgroups/', BandListView.as_view(), name='list_bands'),
    path('add/', BandCreateView.as_view(), name='add_band'),
    path('<slug:slug>', BandDetailView.as_view(), name='band_detail'),
    path('edit/<slug:slug>', BandUpdateView.as_view(), name='edit_band'),
    path('manage/<slug:slug>', ManageBandView.as_view(), name='manage_band'),
    path('ajax_calls/search/', autocomplete_username, name='search'),
    path('add_member/submit', AddMemberView.as_view(), name='add_member'),
    path('delete_member/<int:pk>', MembershipDelete.as_view(), name='del_member'),
    path('change_owner/submit', change_owner, name='change_owner'),
    path('delete_band/<int:pk>', BandDeleteView.as_view(), name='del_band')

]