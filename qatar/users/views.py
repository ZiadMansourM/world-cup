from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import (
    authenticate, 
    login as auth_login,
    logout as auth_logout,
    get_user_model
)

# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username.lower(), password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        messages.error(request, 'Wrong Credentials! Please try again...')
    return render(request, 'users/login.html', {
        'title': 'Login',
        'page': 'login'
    })


def register(request):
    if request.method == 'POST':
        password_one = request.POST['password-one']
        password_two = request.POST['password-two']
        if password_one == password_two:
            username = request.POST['username']
            User = get_user_model()
            if User.objects.filter(username=username.lower()).exists():
                messages.error(request, 'Username already exists!')
            else:
                user = User.objects.create_user(
                    username=username.lower(),
                    password=password_one
                )
                user.save()
                messages.success(request, 'You are now registered and can log in ^^')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match!')
    return render(request, 'users/register.html', {
        'title': 'Register',
        'page': 'register'
    })

def logout(request):
    auth_logout(request)
    return redirect('home')