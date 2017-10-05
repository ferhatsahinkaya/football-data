import boto3
import json
import requests

def handler(event, context):
    sns_client = boto3.client('sns')

    response = requests.get('http://api.football-data.org/v1/competitions')
    competitions = json.loads(response.content.decode('utf-8'))

    for competition in competitions:
        sns_client.publish(
            TopicArn='arn:aws:sns:eu-west-2:907683024242:CompetitionTopic',
            Message=json.dumps({
                'default': json.dumps(competition)
            }),
            MessageStructure='json')

    return None