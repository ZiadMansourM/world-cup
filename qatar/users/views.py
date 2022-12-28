import datetime
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import (
    authenticate, 
    login as auth_login,
    logout as auth_logout,
    get_user_model
)
from django.contrib.auth.decorators import login_required
from main.models import Ticket

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

@login_required(login_url='login')
def profile(request):
    user = request.user
    if request.method == 'POST':
        if request.POST.get('ticket-id'):
            ticket_id = request.POST['ticket-id']
            ticket = Ticket.objects.get(id=ticket_id)
            ticket.delete()
            messages.success(request, 'Ticket deleted successfully!')
            return redirect('profile')
        if request.POST.get('password-one', False) and request.POST.get('password-two', False):
            password_one = request.POST['password-one']
            password_two = request.POST['password-two']
            if password_one == password_two:
                user.set_password(password_one)
                user.save()
                messages.success(request, 'Password updated successfully!')
            else:
                messages.error(request, 'Passwords do not match!')
            return redirect('profile')
        username = request.POST['username']
        email = request.POST['email'] or ""
        gender = int(request.POST['gender']) if request.POST['gender'] else None
        nationality = request.POST['nationality'] or None
        birthday = (
            datetime.datetime.strptime(request.POST['birthday'], "%B %d, %Y").strftime("%Y-%m-%d") 
            if request.POST['birthday'] else None
        )
        User = get_user_model()
        if (
            user.username != username
            and User.objects.filter(username=username.lower()).exists()
        ):
            messages.error(request, 'Username already exists!')
        else:
            args = {
                'email': email,
                'gender': gender, 
                'nationality': nationality,
                'birthday': birthday
            }
            args.update({'username': username.lower()}) if username != user.username else None
            for key, value in args.items():
                setattr(user, key, value)
            user.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    tickets = Ticket.objects.filter(owner=user)
    return render(request, 'users/profile.html', {
        'user': user,
        'tickets': tickets,
        'title': 'Profile',
        'page': 'profile'
    })

def logout(request):
    auth_logout(request)
    return redirect('home')