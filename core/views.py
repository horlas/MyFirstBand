from django.shortcuts import render, redirect
from authentication.models import User
from musicians.models import UserProfile

# Create your views here.


def accueil(request):
    context = {}
    last_user = User.objects.all()[:6]
    context['last_users'] = last_user

    return render(request, 'core/index.html', context)


