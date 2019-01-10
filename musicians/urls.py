from . import views
# from .views import ProfileUpdateView
from django.urls import path

app_name = 'musicians'

urlpatterns = [

    path('profile/', views.profile, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    # path('update_location/', views.update_location, name='update_location')

]