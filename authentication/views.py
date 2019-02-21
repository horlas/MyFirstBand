from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView

# Create your views here.


class SignupCustomView(SuccessMessageMixin, CreateView):

    form_class = SignupForm
    template_name = 'authentication/signup.html'

    def form_valid(self, form):
        next = self.request.POST['next']
        user = form.save()
        user.refresh_from_db()
        raw_password = form.cleaned_data.get('password1')
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect(next)


def logout_view(request):
    # cf : https://docs.djangoproject.com/fr/2.1/topics/auth/default/#how-to-log-a-user-out
    logout(request)
    messages.success(request, ('Vous etes déconnecté'))
    return redirect('core:accueil')

