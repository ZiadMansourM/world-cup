from django import http
from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'main/home.html', {
        'title': 'home',
        'page': 'home'
    })

def match_list(request):
    return render(request,'main/match-list.html', {
        'title': 'Matches',
        'page': 'matches'
    })