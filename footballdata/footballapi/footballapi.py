import json
import logging
import requests

headers = {'X-Auth-Token': 'a076b21e36044e88830990b9ffe2bb04', 'X-Response-Control': 'minified'}
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_competitions():
    competitions_response = requests.get('http://api.football-data.org/v1/competitions', headers=headers)
    competitions = json.loads(competitions_response.content.decode('utf-8'))
    logging.debug(competitions)

    return competitions


def get_standing(competition_id):
    league_table = get_league_table(competition_id)

    standing = None
    if 'standing' in league_table:
        standing = {item['teamId']: item['rank'] for item in league_table['standing']}

    logging.debug('standing: ' + json.dumps(standing))
    return standing


def get_league_table(competition_id):
    league_table_response = requests.get(
        'http://api.football-data.org/v1/competitions/{}/leagueTable'.format(competition_id), headers=headers)
    league_table = json.loads(league_table_response.content.decode('utf-8'))
    logging.debug('league_table: ' + json.dumps(league_table))

    return league_table


def get_next_week_matches(competition_id):
    fixtures = get_fixtures(competition_id)
    future_matches = [match for match in fixtures['fixtures'] if match['status'] not in ['FINISHED', 'CANCELED']]

    current_week = future_matches[0]['matchday'] if future_matches else None

    next_week_matches = [match for match in future_matches if match['matchday'] == current_week]

    logging.debug('next_week_matches: ' + json.dumps(next_week_matches))
    return next_week_matches


def get_fixtures(competition_id):
    fixtures_response = requests.get(
        'http://api.football-data.org/v1/competitions/{}/fixtures'.format(competition_id), headers=headers)
    fixtures = json.loads(fixtures_response.content.decode('utf-8'))
    logging.debug('fixtures: ' + json.dumps(fixtures))

    return fixtures
