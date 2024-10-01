import json
import requests

def lambda_handler(event, context):
    """ AWS Lambda function handler that triggers a backup process 
        to save data on weather forecast in Haifa """
    api_url = "http://18.197.175.10:8200/api/backuphaifa"

    try:
        response = requests.get(api_url)
        response.raise_for_status()

        if response.status_code == 200:
            return {
                'statusCode': 200,
                'body': json.dumps('Backup successful')
            }
        return {
            'statusCode': response.status_code,
            'body': json.dumps('Failed to backup data')
        }

    except requests.RequestException as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }