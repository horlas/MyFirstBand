from . import views
from django.urls import path

app_name = 'authentification'

urlpatterns = [

    path('signin/', views.signin, name='signin'),

]