from django.shortcuts import render

# Create your views here.
def signin(request):
    context = {
        'days': [1 , 2 , 3],
    }
    return render(request, 'authentification/signin.html', context)