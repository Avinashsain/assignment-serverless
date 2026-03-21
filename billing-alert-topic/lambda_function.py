import boto3
from datetime import datetime, timedelta

cloudwatch = boto3.client('cloudwatch')
sns = boto3.client('sns')

SNS_TOPIC_ARN = "arn:aws:sns:ap-south-1:251478238405:billing-alert-topic"
THRESHOLD = 50

def lambda_handler(event, context):

    end = datetime.utcnow()
    start = end - timedelta(days=1)

    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/Billing',
        MetricName='EstimatedCharges',
        Dimensions=[
            {
                'Name': 'Currency',
                'Value': 'USD'
            }
        ],
        StartTime=start,
        EndTime=end,
        Period=86400,
        Statistics=['Maximum']
    )

    if response['Datapoints']:
        amount = response['Datapoints'][0]['Maximum']
        print(f"Current Billing: ${amount}")

        if amount > THRESHOLD:
            message = f"AWS Billing Alert! Current charges: ${amount}"

            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Message=message,
                Subject="AWS Billing Alert"
            )

            print("Alert sent!")
        else:
            print("Billing under control")

    else:
        print("No billing data found")