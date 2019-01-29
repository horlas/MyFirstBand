from band.views import BandListView, UpdateBandView, UpdateProfileBandView
from django.urls import path

app_name = 'band'

urlpatterns = [

    path('listgroups/', BandListView.as_view(), name='list_bands'),
    path('update_groups/', UpdateBandView.as_view(), name='update_band'),
    path('update_band_data/submit', UpdateProfileBandView.as_view(), name='update_profile_data'),

]