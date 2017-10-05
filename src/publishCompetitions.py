import boto3
import json
import logging
import os
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)
headers = {'X-Auth-Token': os.environ['footballApiToken'], 'X-Response-Control': 'minified'}


def handler(event, context):
    sns_client = boto3.client('sns')

    competitions_response = requests.get('http://api.football-data.org/v1/competitions', headers=headers)
    competitions = json.loads(competitions_response.content.decode('utf-8'))
    print('competitions: ' + json.dumps(competitions))

    for competition in competitions:
        sns_client.publish(
            TopicArn=os.environ['competitionTopic'],
            Message=json.dumps({
                'default': json.dumps(competition)
            }),
            MessageStructure='json')

    return None


if __name__ == "__main__":
    handler(None, None)
