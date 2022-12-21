import string
import uuid
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms import ValidationError
from django.utils import timezone
from django.db.models import Q

# Create your models here.
class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'teams'

class Venue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, unique=True)
    rows_num = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(26)])
    seats_num = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    @property
    def size(self):
        return f"A:{string.ascii_uppercase[self.rows_num-1]}x{self.seats_num}={self.rows_num*self.seats_num}"

    def save(self, *args, **kwargs):
        Seat.objects.filter(venue=self).delete()
        for row in range(1, self.rows_num+1):
            for seat in range(1, self.seats_num+1):
                Seat.objects.create(venue=self, row=row, seat=seat)
        super(Venue, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} <{self.size}>"
    
    class Meta:
        db_table = 'venues'

class Seat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    row = models.IntegerField()
    seat = models.IntegerField()

    @property
    def seat_name(self):
        return f'{string.ascii_uppercase[self.row-1]}{self.seat-1}'
    
    def __str__(self):
        return self.seat_name
    
    class Meta:
        db_table = 'seats'

class Referee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'referees'

class Match(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team_one = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_one')
    team_two = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_two')
    score_one = models.IntegerField(default=0)
    score_two = models.IntegerField(default=0)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    level_price = models.DecimalField(max_digits=5, decimal_places=2, default=4.99)
    date_time = models.DateTimeField()
    main_referee = models.ForeignKey(Referee, on_delete=models.CASCADE, related_name='main_referee')
    line_referee_one = models.ForeignKey(Referee, on_delete=models.CASCADE, related_name='line_referee_one')
    line_referee_two = models.ForeignKey(Referee, on_delete=models.CASCADE, related_name='line_referee_two')

    @property
    def result(self):
        return f'{self.team_one}: {self.score_one} - {self.score_two}: {self.team_two}'

    def clean(self):
        if self.main_referee == self.line_referee_one or self.main_referee == self.line_referee_two or self.line_referee_one == self.line_referee_two:
            raise ValidationError("Each referee must be assigned only one role in a match!")
        if self.team_one == self.team_two:
            raise ValidationError("A team cannot play against itself!")
        if self.date_time.date() < timezone.now().date():
            raise ValidationError("The match date and time must be in the future!")
        # Teams Validation: no team can play more than one match per day
        first_team_matches = Match.objects.filter(Q(team_one=self.team_one) | Q(team_two=self.team_one))
        second_team_matches = Match.objects.filter(Q(team_one=self.team_two) | Q(team_two=self.team_two))
        for match in first_team_matches:
            if match.date_time.date() == self.date_time.date():
                raise ValidationError(f"Team {self.team_one} is already playing at this day <Match: {match} @{match.date_time.date()}> !")
        for match in second_team_matches:
            if match.date_time.date() == self.date_time.date():
                raise ValidationError(f"Team {self.team_two} is already playing at this day <Match: {match} @{match.date_time.date()}> !")
        # Referees Validation: no referee can take a role in more than one match per day
        main_referee_matches = Match.objects.filter(
            Q(main_referee=self.main_referee) | Q(line_referee_one=self.main_referee) | Q(line_referee_two=self.main_referee)
        )
        line_referee_one_matches = Match.objects.filter(
            Q(main_referee=self.line_referee_one) | Q(line_referee_one=self.line_referee_one) | Q(line_referee_two=self.line_referee_one)
        )
        line_referee_two_matches = Match.objects.filter(
            Q(main_referee=self.line_referee_two) | Q(line_referee_one=self.line_referee_two) | Q(line_referee_two=self.line_referee_two)
        )
        for match in main_referee_matches:
            if match.date_time.date() == self.date_time.date():
                raise ValidationError(f"Main Referee {self.main_referee} is already refereeing at this day <Match: {match} @{match.date_time.date()}> !")
        for match in line_referee_one_matches:
            if match.date_time.date() == self.date_time.date():
                raise ValidationError(f"Line Referee {self.line_referee_one} is already refereeing at this day <Match: {match} @{match.date_time.date()}> !")
        for match in line_referee_two_matches:
            if match.date_time.date() == self.date_time.date():
                raise ValidationError(f"Line Referee {self.line_referee_two} is already refereeing at this day <Match: {match} @{match.date_time.date()}> !")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.team_one} vs {self.team_two}'

    class Meta:
        db_table = 'matches'
        verbose_name_plural = 'Matches'

class Ticket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)

    @property
    def price(self):
        return self.match.venue.rows_num*self.match.level_price - ((self.seat.row-1)*self.match.level_price)

    def clean(self):
        tickets = Ticket.objects.filter(match=self.match)
        for ticket in tickets:
            if ticket.seat == self.seat:
                raise ValidationError(f"Seat <{self.seat}> is already taken in this match!")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.seat.seat_name} @Match: {self.match}'

    class Meta:
        db_table = 'tickets'