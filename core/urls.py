from . import views
from django.urls import path

app_name = 'core'

urlpatterns = [

    path('', views.accueil, name='accueil'),
    path('band_public/<slug:slug>', views.BandProfileView.as_view(), name='band_profile'),
    path('musician_public/<int:pk>', views.MusicianProfileView.as_view(), name='musician_profile'),
    path('privacy', views.privacy, name='privacy'),
    path('ajax_call/search', views.search, name='search'),
    path('search', views.invite_search, name='invite_search'),
    path('about', views.about, name='about')

]