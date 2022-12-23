from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import (
    authenticate, 
    login as auth_login,
    logout as auth_logout
)

# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        messages.error(request, 'Wrong Credentials! Please try again...')
    return render(request, 'users/login.html', {
        'title': 'Login',
        'page': 'login'
    })


def register(request):
    return render(request, 'users/register.html', {
        'title': 'Register',
        'page': 'register'
    })

def logout(request):
    auth_logout(request)
    return redirect('home')