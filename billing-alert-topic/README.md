# Assignment 6: Monitor and Alert High AWS Billing Using AWS Lambda, Boto3, and SNS

## Objective

Create an automated alerting system that notifies you when AWS billing exceeds a defined threshold.

---

# Architecture

CloudWatch Billing Metrics
⬇
AWS Lambda (Python + Boto3)
⬇
SNS Topic (Email Alert)

---

# Step 1: SNS Setup

1. Go to **AWS Console → SNS**
2. Click **Create Topic**
3. Choose **Standard**
4. Name:

```
billing-alert-topic
```

5. Create Subscription:

   * Protocol: Email
   * Endpoint: your email

6. Confirm subscription from your email inbox

Screenshot
![SNS Topic](screenshots/sns-topic.png)

---

# Step 2: Create IAM Role for Lambda

1. Go to **IAM → Roles**
2. Click **Create Role**
3. Choose **Lambda**
4. Attach policies:

```
CloudWatchFullAccess
AmazonSNSFullAccess
```

5. Role name:

```
lambda-billing-role
```

Screenshot
![IAM Role](screenshots/iam-role-billing.png)

---

# Step 3: Create Lambda Function

1. Go to **AWS Lambda**
2. Click **Create Function**
3. Choose **Author from scratch**

Configuration:

```
Function Name: lambda-billing-function
Runtime: Python 3.x
Execution Role: lambda-billing-role
```

Screenshot
![Lambda Create](screenshots/lambda-create.png)

---

# Step 4: Lambda Function Code

```python
import boto3
from datetime import datetime, timedelta

cloudwatch = boto3.client('cloudwatch')
sns = boto3.client('sns')

SNS_TOPIC_ARN = "YOUR_SNS_TOPIC_ARN"
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
```

Screenshot
![Lambda Code](screenshots/lambda-code-billing.png)

---

# Step 5: Create EventBridge Schedule (Bonus)

1. Go to **EventBridge**
2. Click **Create Rule**
3. Choose **Schedule**

Configuration:

```
Rate: 1 day
```

4. Target:

   * Lambda Function → `lambda-billing-function`

Screenshot
![Event Rule](screenshots/event-rule-billing.png)

---

# Step 6: Test Lambda Function

1. Click **Deploy**
2. Click **Test**
3. Create test event:

```
Event Name: test
```

Screenshot
![Lambda Test](screenshots/lambda-test-billing.png)

---

# Step 7: Verify Email Alert

If billing exceeds threshold:

* You will receive an email notification

Screenshot
![Email Alert](screenshots/email-alert.png)

---

# Step 8: CloudWatch Logs

Go to:

**Lambda → Monitor → View CloudWatch Logs**

Expected output:

```
Current Billing: $0.0
Alert sent!
```

Screenshot
![CloudWatch Logs](screenshots/cloudwatch-logs-billing.png)

---

# Folder Structure

```
aws-billing-alert/
│
├── README.md
|──lambda_function.py
└── screenshots/
    ├── sns-topic.png
    ├── iam-role-billing.png
    ├── lambda-create.png
    ├── lambda-code-billing.png
    ├── event-rule-billing.png
    ├── lambda-test-billing.png
    ├── email-alert.png
    └── cloudwatch-logs-billing.png
```

---

# Expected Result

* Lambda runs daily
* Checks billing amount
* Sends alert if threshold exceeded
* Logs activity in CloudWatch

---

# Conclusion

This project demonstrates how to:

* Monitor AWS billing using CloudWatch
* Automate alerts using Lambda
* Notify users via SNS

---

# Future Improvements

* Add multiple alert thresholds
* Integrate with Slack or Teams
* Store billing data in S3
* Use cost anomaly detection