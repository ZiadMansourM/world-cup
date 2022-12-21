from django.contrib import admin
from main import models

# Register your models here.
admin.site.site_header = 'Qatar World Cup Administration'
admin.site.site_title = 'Qatar 22'

class SeatInline(admin.TabularInline):
    model = models.Seat
    extra = 1

@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):
    include = ('name')
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
    # inlines = [MatchInline]

@admin.register(models.Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'size')
    search_fields = ('name',)
    ordering = ('name',)
    # readonly_fields = ('rows_num', 'seats_num')

@admin.register(models.Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('venue', 'seat_name')
    search_fields = ('venue',)
    ordering = ('venue', 'row', 'seat')

@admin.register(models.Referee)
class RefereeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(models.Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('venue', 'team_one', 'team_two', 'result')
    search_fields = ('venue__name', 'team_one__name', 'team_two__name',)
    ordering = ('venue',)

    def result(self, obj):
        return f'{obj.score_one} - {obj.score_two}'
    result.short_description = 'Match Result'

@admin.register(models.Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('match', 'seat', 'price')
    search_fields = ('match__venue__name', 'seat__venue__name', 'seat__seat_name')
    ordering = ('match', 'seat')