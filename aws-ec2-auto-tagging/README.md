# Assignment 5: Auto-Tagging EC2 Instances on Launch Using AWS Lambda and Boto3

## Objective

Automatically tag EC2 instances at launch using AWS Lambda.

------------------------------------------------------------------------

# Architecture

EC2 Launch → EventBridge → Lambda → Auto Tagging

------------------------------------------------------------------------

# Step 1: EC2 Setup

Go to AWS EC2 dashboard.

Screenshot ![EC2 Dashboard](screenshots/ec2-dashboard.png)

------------------------------------------------------------------------

# Step 2: IAM Role

Policy: AmazonEC2FullAccess

Role Name: LambdaEC2AutoTagRole

Screenshot ![IAM Role](screenshots/iam-role-ec2.png)

------------------------------------------------------------------------

# Step 3: Lambda Function

Function Name: auto-tagging-function\
Runtime: Python 3.x

Screenshot ![Lambda Create](screenshots/lambda-create.png)

------------------------------------------------------------------------

# Step 4: Code

``` python
import boto3
import json
from datetime import datetime

# Initialize the EC2 client outside the handler for better performance (TCP Warm Start)
ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    # 1. Log the incoming event for debugging
    print("Received event:", json.dumps(event))

    try:
        # 2. Extract Instance ID from the EventBridge structure
        # Matches the 'EC2 Instance State-change Notification' format
        instance_id = event.get('detail', {}).get('instance-id')

        if not instance_id:
            print("No Instance ID found in event. Exiting.")
            return {
                'statusCode': 400,
                'body': 'Missing instance-id'
            }

        # 3. Define the Tags
        today = datetime.utcnow().strftime('%Y-%m-%d')
        tags = [
            {'Key': 'LaunchDate', 'Value': today},
            {'Key': 'HeroVired', 'Value': 'DevOps-Avinash'},
            {'Key': 'ManagedBy', 'Value': 'Lambda-Automation'}
        ]

        # 4. Apply Tags to the EC2 Instance
        ec2.create_tags(
            Resources=[instance_id],
            Tags=tags
        )

        success_msg = f"Successfully tagged instance {instance_id}"
        print(success_msg)
        
        return {
            'statusCode': 200,
            'body': json.dumps(success_msg)
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Internal Error: {str(e)}")
        }
```

Screenshot ![Lambda Code](screenshots/lambda-code-ec2.png)

------------------------------------------------------------------------

# Step 5: EventBridge Rule

Event: EC2 → State change → running

Screenshot ![Event Rule](screenshots/event-rule.png)

------------------------------------------------------------------------

# Step 6: Add Target

Lambda: ec2-auto-tag

Screenshot ![Event Target](screenshots/event-target.png)

------------------------------------------------------------------------

# Step 7: Test

Launch EC2 instance

Screenshot ![EC2 Launch](screenshots/ec2-launch.png)

------------------------------------------------------------------------

# Step 8: Verify

Check Tags:

LaunchDate → Date\
HeroVired → DevOps-Avinash\
ManagedBy → Lambda-Automation

Screenshot ![EC2 Tags](screenshots/ec2-tags.png)

------------------------------------------------------------------------

# Step 9: CloudWatch Logs

1.  Go to Lambda → Monitor
2.  Click **View CloudWatch Logs**
3.  Open latest log stream

Expected Logs:

    START RequestId: xxxx
    Tagged instance i-1234567890
    END RequestId: xxxx
    REPORT RequestId: xxxx Duration: 120 ms

Screenshots

![CloudWatch Open](screenshots/cloudwatch-open.png)\
![Log Group](screenshots/log-group.png)\
![Log Stream](screenshots/log-stream.png)\
![Log Output](screenshots/log-output.png)

# Folder Structure

    aws-ec2-auto-tagging/
    ├── README.md
    ├──lambda_function.py
    └── screenshots/