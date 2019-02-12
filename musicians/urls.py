from . import views
from django.urls import path

app_name = 'musicians'

urlpatterns = [

    path('public_profile/<int:pk>', views.public_profile, name='public_profile'),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('update_profile/<int:pk>', views.UpdateProfilView.as_view(), name='update_profile'),
    path('update_avatar/submit', views.UpdateAvatarView.as_view(), name='update_avatar'),
    path('update_data/submit', views.UpdateDataView.as_view(), name='update_data'),
    path('update_location/submit', views.UpdateLocalView.as_view(), name='update_location'),
    path('add_instru/submit', views.InstruCreateView.as_view(), name='add_instru'),
    path('delete_instru/submit', views.InstruDeleteView.as_view(), name='del_instru'),


]