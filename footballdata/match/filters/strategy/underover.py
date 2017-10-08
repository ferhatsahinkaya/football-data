import logging
from footballapi import footballapi
from functools import reduce

from ..domain.filterresult import FilterResult

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def combine_stats(home_team_stats, away_team_stats):
    return {
        'under_or_equal_chance':
            (home_team_stats['under_or_equal_chance'] * away_team_stats['under_or_equal_chance']) / 100,
        'over_or_equal_chance':
            (home_team_stats['over_or_equal_chance'] * away_team_stats['over_or_equal_chance']) / 100
    }


def has_probability(team_stats, expected_chance):
    return team_stats['under_or_equal_chance'] >= expected_chance \
           or team_stats['over_or_equal_chance'] >= expected_chance


def get_matches(competition, filter):
    matches = footballapi.get_next_week_matches(competition['id'])
    number_of_goals = filter['numberofgoals']
    chance = filter['percent']

    selected_match_and_stats = [
        {
            'match': match,
            'stats': combine_stats(
                get_over_under_stats(match['homeTeamId'], number_of_goals),
                get_over_under_stats(match['awayTeamId'], number_of_goals))
        } for match in matches]

    return FilterResult(competition['caption'],
                        [Match(match_and_stats['match']['date'], match_and_stats['match']['homeTeamName'],
                               match_and_stats['match']['awayTeamName'], match_and_stats['stats'])
                         for match_and_stats in selected_match_and_stats
                         if has_probability(match_and_stats['stats'], chance)])


def get_goal_count(match):
    return match['result']['goalsHomeTeam'] + match['result']['goalsAwayTeam']


def get_over_under_stats(team_id, number_of_goals):
    fixtures = footballapi.get_team_fixtures(team_id)

    finished_games = [match for match in fixtures if match['status'] == 'FINISHED']
    finished_game_count = len(finished_games)

    results = reduce(lambda r1, r2:
                     Results(r1.under_or_equal_count + r2.under_or_equal_count,
                             r1.over_or_equal_count + r2.over_or_equal_count)
                     , [Results(
            1 if get_goal_count(match) <= number_of_goals else 0,
            1 if get_goal_count(match) >= number_of_goals else 0) for match in finished_games])

    return {
        'under_or_equal_chance':
            (results.under_or_equal_count / finished_game_count) * 100 if finished_game_count > 0 else 0,
        'over_or_equal_chance':
            (results.over_or_equal_count / finished_game_count) * 100 if finished_game_count > 0 else 0
    }


class Match:
    def __init__(self, datetime, home_team, away_team, stats):
        self.datetime = datetime
        self.homeTeam = home_team
        self.away_team = away_team
        self.stats = stats

    def __str__(self):
        return '{} {} - {} (under_or_equal_chance:{}%, over_or_equal_chance: {}%)' \
            .format(self.datetime, self.homeTeam, self.away_team, self.stats['under_or_equal_chance'],
                    self.stats['over_or_equal_chance'])


class Results:
    def __init__(self, under_or_equal_count, over_or_equal_count):
        self.under_or_equal_count = under_or_equal_count
        self.over_or_equal_count = over_or_equal_count