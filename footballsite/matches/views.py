from django.shortcuts import render

from matchfinder.footballapi import test


def index(request):
    context = {'matches': test.test()}
    return render(request, 'matches/index.html', context)
