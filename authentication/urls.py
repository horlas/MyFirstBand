from . import views
from django.urls import path, include, reverse_lazy
from django.contrib.auth import views as auth_views
from .forms import CustomLoginForm

app_name = 'authentication'

urlpatterns = [
    path('signup/', views.SignupCustomView.as_view(), name='signup'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='authentication/login.html',
                                                          authentication_form=CustomLoginForm), name='login'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(
                                                    template_name='authentication/password_reset_form.html',
                                                    email_template_name='authentication/reset_password_email.html',
                                                    subject_template_name='authentication/reset_password_subject.txt',
                                                    success_url= reverse_lazy('authentication:reset_password_done'),
                                                    ) ,name='password_reset'),
    path('accounts/password_reset_done/', auth_views.PasswordResetDoneView.as_view(
                                            template_name='authentication/password_reset_done.html'), name='reset_password_done'),
    path('accounts/password_reset_confirm/<uidb64>/<token>/ ', auth_views.PasswordResetConfirmView.as_view(
                                                            template_name='authentication/password_reset_confirm.html',
                                                            success_url= reverse_lazy('authentication:reset_password_complete'),
                                                            post_reset_login_backend='django.contrib.auth.backends.ModelBackend',
                                                            post_reset_login=True ), name='reset_password_confirm'),
    path('accounts/password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='authentication/password_reset_complete.html'),
                                                                                            name='reset_password_complete'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('social_django.urls', namespace='social'))

]