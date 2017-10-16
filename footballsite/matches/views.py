from django.shortcuts import render
from matchfinder.filter import filtermatch
from matchfinder.footballapi import footballapi


def index(request):
    filter = {'type': 'topbottom', 'percent': 20}

    competitions = footballapi.get_competitions()
    competitions = [competition for competition in competitions]

    result = [filtermatch.get_matches(competition, filter) for competition in competitions]
    context = {'competitions': result}

    return render(request, 'matches/index.html', context)
