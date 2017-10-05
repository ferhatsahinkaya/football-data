import requests
import json
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    message = event['Records'][0]['Sns']['Message']
    logger.info('got event message {}'.format(message))

    response = requests.get(message['_links']['fixtures']['href'])
    fixtures = json.loads(response.content.decode('utf-8'))

    future_matches = [match for match in fixtures['fixtures'] if match['status'] != 'FINISHED']

    current_week = future_matches[0]['matchday'] if future_matches else None

    next_week_matches = [match for match in future_matches if match['matchday'] == current_week]

    logging.info('next_week_matches: ' + json.dumps(next_week_matches))

    return None

# if __name__ == "__main__":
#     handler({
#         'Records': [{'Sns': {'Message': {'_links': {'fixtures': {'href': 'http://api.football-data.org/v1/competitions/446/fixtures'}}}}}]
#     }, None)