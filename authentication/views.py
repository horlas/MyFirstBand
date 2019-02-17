from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import SignupForm

# Create your views here.
def signup(request):

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username=user.username, password=raw_password)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('core:accueil')
    else:
        form = SignupForm()

    return render(request, 'authentication/signup.html', {'form': form})


def logout_view(request):
    # cf : https://docs.djangoproject.com/fr/2.1/topics/auth/default/#how-to-log-a-user-out
    logout(request)
    messages.success(request, ('Vous etes déconnecté'))
    return redirect('core:accueil')

