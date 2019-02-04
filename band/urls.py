from band.views import *
from django.urls import path

app_name = 'band'

urlpatterns = [

    path('listgroups/', BandListView.as_view(), name='list_bands'),
    path('add/', BandCreateView.as_view(), name='add_band'),
    path('<slug:slug>', BandDetailView.as_view(), name='band_detail'),
    path('edit/<slug:slug>', BandUpdateView.as_view(), name='edit_band'),

]