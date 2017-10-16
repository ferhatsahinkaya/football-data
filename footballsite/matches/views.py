from django.shortcuts import render
from matchfinder.filter import filtermatch
from matchfinder.footballapi import footballapi

pages = {
    'topbottom': 'competitions_topbottom.html',
    'underover': 'competitions_underover.html'
}

def index(request):
    context = {'filters': [
        {'type': 'topbottom'},
        {'type': 'underover'}
    ]}

    return render(request, 'matches/index.html', context)


def find_competitions(request):
    filter_type = request.GET['filter_type']
    if filter_type == 'topbottom':
        filter = {'type': filter_type, 'percent': int(request.GET['percent'])}
    else:
        filter = {'type': filter_type, 'percent': int(request.GET['percent']),
                  'numberofgoals': int(request.GET['numberofgoals']), 'homeaway': request.GET['homeaway'] == 'on',
                  'halftime': request.GET['halffulltime'] == 'halftime'}

    competitions = footballapi.get_competitions()
    competitions = [competition for competition in competitions]

    result = [filtermatch.get_matches(competition, filter) for competition in competitions]
    context = {'competitions': result}

    return render(request, 'matches/' + pages[filter_type], context)
