# Assignment 7: DynamoDB Item Change Alert Using AWS Lambda, Boto3, and SNS

---

## Objective
Automate alerts whenever an item in a DynamoDB table is updated.

---

## Architecture
DynamoDB → DynamoDB Stream → Lambda → SNS → Email

---

## Steps

### 1. DynamoDB Setup
- Create table: `UserTable`
- Partition key: `userId`
- Add sample item

Screenshot:
- ![Dynamodb Table](screenshots/1-dynamodb-table.png)
- ![Dynamodb Items](screenshots/2-dynamodb-items.png)

---

### 2. Enable DynamoDB Streams
- Enable stream
- Select: **New and old images**

Screenshot:
- ![Dynamodb Stream](screenshots/3-dynamodb-stream.png)

---

### 3. SNS Setup
- Create topic: `DynamoDB-Alerts`
- Subscribe email
- Confirm subscription

- Screenshot ![SNS Topic](screenshots/4-sns-topic.png)
- Screenshot ![SNS Subscription](screenshots/5-sns-subscription.png)

---

### 4. IAM Role
- Create role for Lambda
- Attach policies:
  - AmazonDynamoDBFullAccess
  - AmazonSNSFullAccess
  - CloudWatchFullAccess

- Screenshot ![IAM Role](screenshots/6-iam-role.png)

---

### 5. Lambda Function
- Runtime: Python 3.x
- Attach IAM role

```python
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
            message += "Old Value:\n" + json.dumps(old_image, indent=2)
            message += "\n\nNew Value:\n" + json.dumps(new_image, indent=2)

            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject="DynamoDB Item Updated Alert",
                Message=message
            )

    return {
        'statusCode': 200,
        'body': 'Notification Sent'
    }
```

- Screenshot ![Lambda Code](screenshots/7-lambda-code.png)

---

### 6. Add Trigger
- Add DynamoDB trigger to Lambda

- Screenshot ![Lambda Trigger](screenshots/8-lambda-trigger.png)

---

### 7. Testing
- Update item in DynamoDB

Example:
- age: 40 → 26

- Screenshot ![Testing](screenshots/9-dynamodb-update.png)

---

## Output

### Email Alert
- Screenshot ![Email Alert](screenshots/10-email-alert.png)

### CloudWatch Logs
- Screenshot ![CloudWatch Logs](screenshots/11-cloudwatch-logs.png)

---

## Conclusion
- Successfully captured DynamoDB changes
- Triggered Lambda automatically
- Sent SNS email alert

---

## Notes
- Ensure SNS ARN is correct
- Confirm email subscription
- Check IAM permissions if errors occur