from . import views
# from .views import ProfileUpdateView
from django.urls import path

app_name = 'musicians'

urlpatterns = [

    path('profile/', views.profile, name='profile'),
    path('update_profile/', views.UpdateProfilView.as_view(), name='update_profile'),
    path('update_avatar/', views.UpdateAvatarView.as_view(), name = 'update_avatar'),
    path('update_data', views.UpdateDataView.as_view(), name='update_data'),
    path('update_local', views.UpdateLocalView.as_view(), name='update_local'),

    # path('update_profile/', views.update_profile, name='update_profile'),
    # path('update_location/', views.update_location, name='update_location')

]