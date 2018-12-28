from django.shortcuts import render

# Create your views here.
def signup(request):
    context = {
        'days': [1 , 2 , 3],
    }
    return render(request, 'authentification/signup.html', context)