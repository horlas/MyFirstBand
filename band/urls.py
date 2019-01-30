from band.views import *
from django.urls import path

app_name = 'band'

urlpatterns = [

    path('listgroups/', BandListView.as_view(), name='list_bands'),
    path('group/add/', BandCreateView.as_view(), name='add_band'),

]