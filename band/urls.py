from band.views import BandListView
from django.urls import path

app_name = 'band'

urlpatterns = [

    path('listgroupes/', BandListView.as_view(), name='list_bands'),

]