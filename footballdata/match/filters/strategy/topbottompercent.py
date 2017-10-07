import logging
from footballapi import footballapi
from math import ceil

from ..domain.filterresult import FilterResult
from ..domain.match import Match

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def before_or_equal(team, standing, position):
    return standing[team] <= position


def after_or_equal(team, standing, position):
    return standing[team] >= position


def get_matches(competition, filter):
    selected_matches = []
    standing = footballapi.get_standing(competition['id'])

    if standing:
        number_of_teams = len(standing)
        group_size = ceil(number_of_teams * (filter['value'] / 100))

        matches = footballapi.get_next_week_matches(competition['id'])

        selected_matches = [match for match in matches
                            if (
                                before_or_equal(match['homeTeamId'], standing, group_size)
                                and after_or_equal(match['awayTeamId'], standing,
                                                   number_of_teams - group_size + 1))
                            or (
                                before_or_equal(match['awayTeamId'], standing, group_size)
                                and after_or_equal(match['homeTeamId'], standing,
                                                   number_of_teams - group_size + 1))]

    return FilterResult(competition['caption'],
                        [Match(match['date'], match['homeTeamName'], standing[match['homeTeamId']],
                               match['awayTeamName'], standing[match['awayTeamId']])
                         for match in selected_matches])
