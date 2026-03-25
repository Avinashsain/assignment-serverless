import json
import boto3

sns = boto3.client('sns')

SNS_TOPIC_ARN = "arn:aws:sns:ap-south-1:XXXXXXXXXXXX:DynamoDB-Alerts"

def lambda_handler(event, context):
    
    print("Event Received:", json.dumps(event))
    
    for record in event['Records']:
        
        if record['eventName'] == 'MODIFY':
            
            old_image = record['dynamodb'].get('OldImage', {})
            new_image = record['dynamodb'].get('NewImage', {})
            
            message = "DynamoDB Item Updated\n\n"
            message += "Old Value:\n"
            message += json.dumps(old_image, indent=2)
            
            message += "\n\nNew Value:\n"
            message += json.dumps(new_image, indent=2)
            
            print("Sending SNS Notification...")
            
            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject="DynamoDB Item Updated Alert",
                Message=message
            )
    
    return {
        'statusCode': 200,
        'body': 'Notification Sent'
    }