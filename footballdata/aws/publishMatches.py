import json
import logging
import os
import requests
from math import ceil

logger = logging.getLogger()
logger.setLevel(logging.INFO)
headers = {'X-Auth-Token': os.environ['footballApiToken'], 'X-Response-Control': 'minified'}


def before_or_equal(team, standing, position):
    return standing[team] <= position


def after_or_equal(team, standing, position):
    return standing[team] >= position


def handler(event, context):
    logger.info('got event {}'.format(event))
    competition = json.loads(event['Records'][0]['Sns']['Message'])

    selected_matches = []
    standing = get_standing(competition)

    if standing:
        number_of_teams = len(standing)
        group_size = ceil(number_of_teams * 0.2)

        matches = get_next_week_matches(competition)

        selected_matches = [match for match in matches
                            if (
                                before_or_equal(match['homeTeamId'], standing, group_size)
                                and after_or_equal(match['awayTeamId'], standing, number_of_teams - group_size + 1))
                            or (
                                before_or_equal(match['awayTeamId'], standing, group_size)
                                and after_or_equal(match['homeTeamId'], standing, number_of_teams - group_size + 1))]

    logger.info(selected_matches)

    return None


def get_next_week_matches(competition):
    fixtures_response = requests.get(
        'http://api.football-data.org/v1/competitions/{}/fixtures'.format(competition['id']), headers=headers)
    fixtures = json.loads(fixtures_response.content.decode('utf-8'))

    future_matches = [match for match in fixtures['fixtures'] if match['status'] not in ['FINISHED', 'CANCELED']]

    current_week = future_matches[0]['matchday'] if future_matches else None

    next_week_matches = [match for match in future_matches if match['matchday'] == current_week]

    logging.info('next_week_matches: ' + json.dumps(next_week_matches))
    return next_week_matches


def get_standing(competition):
    league_table_response = requests.get(
        'http://api.football-data.org/v1/competitions/{}/leagueTable'.format(competition['id']), headers=headers)
    league_table = json.loads(league_table_response.content.decode('utf-8'))

    standing = None
    if 'standing' in league_table:
        standing = {item['teamId']: item['rank'] for item in league_table['standing']}

    logging.info('standing: ' + json.dumps(standing))
    return standing


if __name__ == "__main__":
    handler({
        'Records': [{'EventSource': 'aws:sns', 'EventVersion': '1.0',
                     'EventSubscriptionArn': 'arn:aws:sns:eu-west-2:907683024242:CompetitionTopic:fa972dd0-0d81-4a88-932a-199a5fa28df2',
                     'Sns': {'Type': 'Notification', 'MessageId': '92df5af3-f828-5ff5-95c5-08a3a684d1d0',
                             'TopicArn': 'arn:aws:sns:eu-west-2:907683024242:CompetitionTopic', 'Subject': None,
                             'Message': '{"id": 459, "caption": "Serie B 2017/18", "league": "SB", "year": "2017", "currentMatchday": 8, "numberOfMatchdays": 42, "numberOfTeams": 22, "numberOfGames": 462, "lastUpdated": "2017-10-05T10:00:20Z"}',
                             'Timestamp': '2017-10-05T16:23:08.555Z', 'SignatureVersion': '1',
                             'Signature': 'O4dpGEYXkVeyDRKl8tVe+dz9uihYLrlRrOasxjxQtV0B/fVHhEO1SxCs7L/DsUenJv/lJY4KHe6XtOdKlkP32aNsPtuzIOAS4a8d366iEQe7hoLxb1WZGGIMvYU7CudyBPsoxBu2LquXseDCW4phQR+DlaW0YVQLZEcLQzva7SX0BNlmRvzd1QjczG70hD0XPnn7cclqZM9FJyLmlWpsPS+xqQ72jPDAEepzTfItnNp+jo85cBgi/MbuvJ6BI3r5lCzzN405KJO5rWoR5jStuWAzGViA+O9ksOXUVhJN4GdVkZu1RtQBVVgTfMIN8d1F6deSBIshlyhnk7mPm0DWdw==',
                             'SigningCertUrl': 'https://sns.eu-west-2.amazonaws.com/SimpleNotificationService-433026a4050d206028891664da859041.pem',
                             'UnsubscribeUrl': 'https://sns.eu-west-2.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:eu-west-2:907683024242:CompetitionTopic:fa972dd0-0d81-4a88-932a-199a5fa28df2',
                             'MessageAttributes': {}}}]
    }, None)
