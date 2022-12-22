from django.shortcuts import render
from main.models import Match

# Create your views here.
def home(request):
    return render(request,'main/home.html', {
        'title': 'home',
        'page': 'home'
    })

def match_list(request):
    matches = Match.objects.all()
    return render(request,'main/match-list.html', {
        'matches': matches,
        'title': 'Matches',
        'page': 'matches'
    })