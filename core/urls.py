from . import views
from django.urls import path

app_name = 'core'

urlpatterns = [

path('', views.accueil, name='accueil'),
path('groupe_public/<slug:slug>', views.BandProfileView.as_view(), name='band_profile_public'),

]