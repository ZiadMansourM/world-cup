import string
from django.shortcuts import redirect, render
from main.models import Match, Ticket, Seat
from django.contrib import messages


# Create your views here.
def home(request):
    return render(request,'main/home.html', {
        'title': 'home',
        'page': 'home'
    })

def match_list(request):
    if request.method == 'POST':
        match_id = request.POST.get('match-id')
        seats = request.POST.get('seats').split(',')
        match = Match.objects.get(id=match_id)
        for seat_number in seats:
            seat = Seat.objects.get(
                venue=match.venue,
                row=string.ascii_uppercase.find(seat_number[0])+1,
                seat=int(seat_number[1])+1
            )
            Ticket.objects.create(match=match, seat=seat, owner=request.user)
            messages.success(request, f'Ticket for {seat_number} booked successfully!')
        return redirect('match-list')
    matches = Match.objects.all()
    tickets = Ticket.objects.all()
    for match in matches:
        tickets = Ticket.objects.filter(match=match)
        match.taken_seats = [(ticket.seat.row, ticket.seat.seat) for ticket in tickets]
    return render(request,'main/match-list.html', {
        'matches': matches,
        'tickets': tickets,
        'title': 'Matches',
        'page': 'matches'
    })