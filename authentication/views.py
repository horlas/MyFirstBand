from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView

# Create your views here.

class SignupView(SuccessMessageMixin, CreateView):
    form_class = SignupForm
    template_name = 'authentication/signup.html'
    def get_success_url(self):
        referer_url = self.request.META.get('HTTP_REFERER')
        return referer_url
    def form_valid(self, form):
        user = form.save()
        user.refresh_from_db()
        raw_password = form.cleaned_data.get('password1')
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

# def signup(request):
#
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             user.refresh_from_db()
#             raw_password = form.cleaned_data.get('password1')
#             # user = authenticate(username=user.username, password=raw_password)
#             login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#             referer_url = request.META.get('HTTP_REFERER')
#             return referer_url
#     else:
#         form = SignupForm()
#
#     return render(request, 'authentication/signup.html', {'form': form})


def logout_view(request):
    # cf : https://docs.djangoproject.com/fr/2.1/topics/auth/default/#how-to-log-a-user-out
    logout(request)
    messages.success(request, ('Vous etes déconnecté'))
    return redirect('core:accueil')

