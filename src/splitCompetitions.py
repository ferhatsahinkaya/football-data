import json
import logging
import requests
from math import ceil

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def before_or_equal(team, standing, position):
    return standing[team] <= position


def after_or_equal(team, standing, position):
    return standing[team] >= position


def handler(event, context):
    logger.info('got event {}'.format(event))
    message = json.loads(event['Records'][0]['Sns']['Message'])

    standing = get_standing(message)
    number_of_teams = len(standing)
    group_size = ceil(number_of_teams * 0.2)

    matches = get_matches(message)

    selected_matches = [match for match in matches
                        if (before_or_equal(match['_links']['homeTeam']['href'], standing, group_size) and after_or_equal(match['_links']['awayTeam']['href'], standing, number_of_teams - group_size + 1))
                           or (before_or_equal(match['_links']['awayTeam']['href'], standing, group_size) and after_or_equal(match['_links']['homeTeam']['href'], standing, number_of_teams - group_size + 1))]
    logger.info(selected_matches)

    return None

def get_matches(message):
    fixtures_response = requests.get(message['_links']['fixtures']['href'])
    fixtures = json.loads(fixtures_response.content.decode('utf-8'))

    future_matches = [match for match in fixtures['fixtures'] if match['status'] != 'FINISHED']

    current_week = future_matches[0]['matchday'] if future_matches else None

    next_week_matches = [match for match in future_matches if match['matchday'] == current_week]

    logging.info('next_week_matches: ' + json.dumps(next_week_matches))
    return next_week_matches


def get_standing(message):
    league_table_response = requests.get(message['_links']['leagueTable']['href'])
    league_table = json.loads(league_table_response.content.decode('utf-8'))

    standing = [team['_links']['team']['href'] for team in league_table['standing']]

    standing = {k: v for v, k in enumerate(standing, 1)}
    logging.info('standing' + json.dumps(standing))
    return standing


if __name__ == "__main__":
    handler({
        'Records': [{'Sns': {
            'Message': '{"_links": {"self": {"href": "http://api.football-data.org/v1/competitions/457"}, "teams": {"href": "http://api.football-data.org/v1/competitions/457/teams"}, "fixtures": {"href": "http://api.football-data.org/v1/competitions/457/fixtures"}, "leagueTable": {"href": "http://api.football-data.org/v1/competitions/457/leagueTable"}}, "id": 457, "caption": "Primeira Liga 2017/18", "league": "PPL", "year": "2017", "currentMatchday": 9, "numberOfMatchdays": 34, "numberOfTeams": 18, "numberOfGames": 306, "lastUpdated": "2017-10-04T10:00:16Z"}'}}]
    }, None)
