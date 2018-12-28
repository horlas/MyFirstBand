from . import views
from django.urls import path

app_name = 'authentification'

urlpatterns = [

    path('signup/', views.signup, name='signup'),

]