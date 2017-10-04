# import boto3
import json
import requests

def handler(event, context):
    competitions = json.loads(requests.get('http://api.football-data.org/v1/competitions'))

    # client = boto3.client('sns')

    for competition in competitions:
        print(competition)
        # client.publish(
        #     TopicArn = 'arn:aws:sns:eu-west-2:907683024242:CompetitionTopic',
        #     Message = json.dumps({
        #         'default' : '{}',
        #         'competitions' : competition
        #     }),
        #     MessageStructure='json')

if __name__ == "__publishCompetitions__":
    handler(None, None)