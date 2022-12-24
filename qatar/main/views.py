from django.shortcuts import render
from main.models import Match, Ticket

# Create your views here.
def home(request):
    return render(request,'main/home.html', {
        'title': 'home',
        'page': 'home'
    })

def match_list(request):
    matches = Match.objects.all()
    tickets = Ticket.objects.all()
    for match in matches:
        tickets = Ticket.objects.filter(match=match)
        match.taken_rows = [ticket.seat.row for ticket in tickets]
        match.taken_cols = [ticket.seat.seat for ticket in tickets]
    return render(request,'main/match-list.html', {
        'matches': matches,
        'tickets': tickets,
        'title': 'Matches',
        'page': 'matches'
    })