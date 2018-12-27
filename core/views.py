from django.shortcuts import render, redirect

# Create your views here.

def accueil(request):
    context = {
        'days': [1 , 2 , 3],
    }
    return render(request, 'core/index.html', context)