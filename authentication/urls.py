from . import views
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .forms import CustomLoginForm

app_name = 'authentication'

urlpatterns = [

    path('signup/', views.signup, name='signup'),
    # path('logout/', views.logout_view, name='logout'),
    path ('accounts/login/', auth_views.LoginView.as_view(template_name='authentication/login.html', authentication_form=CustomLoginForm)),
    path ('accounts/', include('django.contrib.auth.urls')),


]