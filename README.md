# Assignment 1: Automated Instance Management Using AWS Lambda and Boto3

## Objective

The goal of this assignment is to automate the starting and stopping of
EC2 instances based on tags using AWS Lambda and Boto3.

------------------------------------------------------------------------

# Architecture

EC2 Instances (Tagged)\
⬇\
AWS Lambda (Python + Boto3)\
⬇\
Automatic Start / Stop

------------------------------------------------------------------------

# Step 1: Create EC2 Instances

1.  Go to AWS Console → EC2 Dashboard
2.  Launch two instances (t2.micro).

### Instance 1

Name: `instance-stop`

Tag:

  Key      Value
  -------- -----------
  Action   Auto-Stop

Screenshot: EC2 instance with Auto-Stop tag

![EC2 Auto Stop](aws-ec2-lambda-automation/screenshots/ec2-auto-stop.png)

------------------------------------------------------------------------

### Instance 2

Name: `instance-start`

Tag:

  Key      Value
  -------- ------------
  Action   Auto-Start

Screenshot: EC2 instance with Auto-Start tag

![EC2 Auto Start](aws-ec2-lambda-automation/screenshots/ec2-auto-start.png)

------------------------------------------------------------------------

# Step 2: Create IAM Role for Lambda

1.  Go to IAM Dashboard
2.  Click Roles → Create Role
3.  Choose Lambda
4.  Attach policy:

AmazonEC2FullAccess

Role Name:

LambdaEC2ManagerRole

Screenshot: IAM role with EC2 permissions

![IAM Role](aws-ec2-lambda-automation/screenshots/iam-role.png)

------------------------------------------------------------------------

# Step 3: Create Lambda Function

1.  Open AWS Lambda Console
2.  Click Create Function
3.  Choose Author From Scratch

Settings:

Function Name: ec2-auto-manager\
Runtime: Python 3.x\
Execution Role: LambdaEC2ManagerRole

Screenshot: Lambda function creation page

![Lambda Create](aws-ec2-lambda-automation/screenshots/lambda-create.png)

------------------------------------------------------------------------

# Step 4: Lambda Function Code

``` python
import boto3

ec2 = boto3.client('ec2')

def lambda_handler(event, context):

    # Stop instances with Auto-Stop tag
    stop_instances = ec2.describe_instances(
        Filters=[
            {'Name': 'tag:Action', 'Values': ['Auto-Stop']},
            {'Name': 'instance-state-name', 'Values': ['running']}
        ]
    )

    stop_ids = []

    for reservation in stop_instances['Reservations']:
        for instance in reservation['Instances']:
            stop_ids.append(instance['InstanceId'])

    if stop_ids:
        ec2.stop_instances(InstanceIds=stop_ids)
        print("Stopping instances:", stop_ids)
    else:
        print("No instances to stop")

    # Start instances with Auto-Start tag
    start_instances = ec2.describe_instances(
        Filters=[
            {'Name': 'tag:Action', 'Values': ['Auto-Start']},
            {'Name': 'instance-state-name', 'Values': ['stopped']}
        ]
    )

    start_ids = []

    for reservation in start_instances['Reservations']:
        for instance in reservation['Instances']:
            start_ids.append(instance['InstanceId'])

    if start_ids:
        ec2.start_instances(InstanceIds=start_ids)
        print("Starting instances:", start_ids)
    else:
        print("No instances to start")

    return {
        'statusCode': 200,
        'body': 'EC2 actions completed'
    }
```

Screenshot: Lambda code editor

![Lambda Code](aws-ec2-lambda-automation/screenshots/lambda-code.png)

------------------------------------------------------------------------

# Step 5: Deploy and Test Lambda

1.  Click Deploy
2.  Click Test
3.  Create test event

Event Name: test

Screenshot: Lambda test execution

![Lambda Test](aws-ec2-lambda-automation/screenshots/lambda-test.png)

------------------------------------------------------------------------

# Step 6: Verify EC2 Results

Go back to EC2 Dashboard and check instance states.

Expected results:

  Instance         Tag          Result
  ---------------- ------------ ---------
  instance-stop    Auto-Stop    Stopped
  instance-start   Auto-Start   Running

Screenshot: EC2 instances state after Lambda execution

![EC2 Result](aws-ec2-lambda-automation/screenshots/ec2-result.png)

------------------------------------------------------------------------

# Case Testing

## Case 1

Initial state:

instance-stop = Stopped\
instance-start = Stopped

Result:

instance-stop = Stopped\
instance-start = Running

------------------------------------------------------------------------

## Case 2

Initial state:

instance-stop = Running\
instance-start = Running

Result:

instance-stop = Stopped\
instance-start = Running

------------------------------------------------------------------------

# Conclusion

This project demonstrates how AWS Lambda and Boto3 can automatically
manage EC2 instances based on tags.

This approach helps automate infrastructure management and reduce manual
work in cloud environments.

------------------------------------------------------------------------
# Assignment 2: Automated S3 Bucket Cleanup Using AWS Lambda and Boto3

## Objective

Automate deletion of files older than **30 days** from an S3 bucket
using AWS Lambda and Boto3.

------------------------------------------------------------------------

# Architecture

S3 Bucket (Files Stored) ↓ AWS Lambda (Python + Boto3) ↓ Delete Files
Older Than 30 Days

------------------------------------------------------------------------

# Step 1: Create S3 Bucket

1.  Go to **AWS Console → S3**
2.  Click **Create Bucket**
3.  Example bucket name:

s3-cleanup-demo-avinash

4.  Upload multiple files.

Ensure: - Some files are **older than 30 days** - Some files are
**recent**

Screenshot

![S3 Files](aws-s3-cleanup-lambda/screenshots/s3-files.png)

------------------------------------------------------------------------

# Step 2: Create IAM Role for Lambda

1.  Open **IAM → Roles**
2.  Click **Create Role**
3.  Select **Lambda**
4.  Attach policy:

AmazonS3FullAccess

5.  Role Name:

LambdaS3CleanupRole

Screenshot

![IAM Role](aws-s3-cleanup-lambda/screenshots/iam-role-s3.png)

------------------------------------------------------------------------

# Step 3: Create Lambda Function

Configuration:

Function Name: s3-cleanup-function\
Runtime: Python 3.x\
Execution Role: LambdaS3CleanupRole

Screenshot

![Lambda Create](aws-s3-cleanup-lambda/screenshots/lambda-create.png)

------------------------------------------------------------------------

# Step 4: Lambda Code

``` python
import boto3
from datetime import datetime, timezone, timedelta

s3 = boto3.client('s3')

BUCKET_NAME = "s3-cleanup-demo-avinash"
DAYS = 30

def lambda_handler(event, context):

    deleted_files = []

    response = s3.list_objects_v2(Bucket=BUCKET_NAME)

    if 'Contents' not in response:
        print("Bucket is empty")
        return

    for obj in response['Contents']:

        file_name = obj['Key']
        last_modified = obj['LastModified']

        file_age = datetime.now(timezone.utc) - last_modified

        if file_age > timedelta(days=DAYS):

            s3.delete_object(
                Bucket=BUCKET_NAME,
                Key=file_name
            )

            deleted_files.append(file_name)
            print(f"Deleted: {file_name}")

    if not deleted_files:
        print("No old files found")

    return {
        'statusCode': 200,
        'deleted_files': deleted_files
    }
```

Screenshot

![Lambda Code](aws-s3-cleanup-lambda/screenshots/lambda-code-s3.png)

------------------------------------------------------------------------

# Step 5: Test Lambda

1.  Click **Deploy**
2.  Click **Test**
3.  Create test event

Event Name: test

Screenshot

![Lambda Test](aws-s3-cleanup-lambda/screenshots/lambda-test-s3.png)

------------------------------------------------------------------------

# Step 6: Verify Results

After running Lambda:

  File Age             Result
  -------------------- ---------
  Older than 30 days   Deleted
  Newer than 30 days   Remains

Screenshot

![S3 Result](aws-s3-cleanup-lambda/screenshots/s3-result.png)

------------------------------------------------------------------------

# Example Logs

Deleted file: Complete Python VS Code Installation Guide for DevOps (2) (1).pdf
Deleted file: Complete Python VS Code Installation Guide for DevOps (2).pdf
Deleted file: MongoDB Atlas + Compass - Complete Setup Guide (Windows macOS) (1).pdf
Deleted file: MongoDB Atlas + Compass - Complete Setup Guide (Windows macOS).pdf
Deleted file: Screenshot 2025-11-01 at 1.00.27 PM.png
Deleted file: Screenshot 2025-11-01 at 1.53.03 PM.png
Deleted file: Screenshot 2025-11-01 at 1.53.07 PM.png
Deleted file: Screenshot 2025-11-01 at 1.56.45 PM.png
Deleted file: Screenshot 2025-11-01 at 12.17.21 PM.png
Deleted file: Screenshot 2025-11-01 at 12.24.55 PM.png
Deleted file: Screenshot 2025-11-01 at 12.36.01 PM.png
Deleted file: Screenshot 2025-11-01 at 12.47.49 PM.png
Deleted file: Screenshot 2025-11-01 at 12.55.18 PM.png

------------------------------------------------------------------------

# Assignment 5: Auto-Tagging EC2 Instances on Launch Using AWS Lambda and Boto3

## Objective

Automatically tag EC2 instances at launch using AWS Lambda.

------------------------------------------------------------------------

# Architecture

EC2 Launch → EventBridge → Lambda → Auto Tagging

------------------------------------------------------------------------

# Step 1: EC2 Setup

Go to AWS EC2 dashboard.

Screenshot ![EC2 Dashboard](aws-ec2-auto-tagging/screenshots/ec2-dashboard.png)

------------------------------------------------------------------------

# Step 2: IAM Role

Policy: AmazonEC2FullAccess

Role Name: LambdaEC2AutoTagRole

Screenshot ![IAM Role](aws-ec2-auto-tagging/screenshots/iam-role-ec2.png)

------------------------------------------------------------------------

# Step 3: Lambda Function

Function Name: auto-tagging-function\
Runtime: Python 3.x

Screenshot ![Lambda Create](aws-ec2-auto-tagging/screenshots/lambda-create.png)

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

Screenshot ![Lambda Code](aws-ec2-auto-tagging/screenshots/lambda-code-ec2.png)

------------------------------------------------------------------------

# Step 5: EventBridge Rule

Event: EC2 → State change → running

Screenshot ![Event Rule](aws-ec2-auto-tagging/screenshots/event-rule.png)

------------------------------------------------------------------------

# Step 6: Add Target

Lambda: ec2-auto-tag

Screenshot ![Event Target](aws-ec2-auto-tagging/screenshots/event-target.png)

------------------------------------------------------------------------

# Step 7: Test

Launch EC2 instance

Screenshot ![EC2 Launch](aws-ec2-auto-tagging/screenshots/ec2-launch.png)

------------------------------------------------------------------------

# Step 8: Verify

Check Tags:

LaunchDate → Date\
HeroVired → DevOps-Avinash\
ManagedBy → Lambda-Automation

Screenshot ![EC2 Tags](aws-ec2-auto-tagging/screenshots/ec2-tags.png)

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

![CloudWatch Open](aws-ec2-auto-tagging/screenshots/cloudwatch-open.png)\
![Log Group](aws-ec2-auto-tagging/screenshots/log-group.png)\
![Log Stream](aws-ec2-auto-tagging/screenshots/log-stream.png)\
![Log Output](aws-ec2-auto-tagging/screenshots/log-output.png)

# Folder Structure

    aws-ec2-auto-tagging/
    ├── README.md
    ├──lambda_function.py
    └── screenshots/

------------------------------------------------------------------------

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
![SNS Topic](billing-alert-topic/screenshots/sns-topic.png)

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
![IAM Role](billing-alert-topic/screenshots/iam-role-billing.png)

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
![Lambda Create](billing-alert-topic/screenshots/lambda-create.png)

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
![Lambda Code](billing-alert-topic/screenshots/lambda-code-billing.png)

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
![Event Rule](billing-alert-topic/screenshots/event-rule-billing.png)

---

# Step 6: Test Lambda Function

1. Click **Deploy**
2. Click **Test**
3. Create test event:

```
Event Name: test
```

Screenshot
![Lambda Test](billing-alert-topic/screenshots/lambda-test-billing.png)

---

# Step 7: Verify Email Alert

If billing exceeds threshold:

* You will receive an email notification

Screenshot
![Email Alert](billing-alert-topic/screenshots/email-alert.png)

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
![CloudWatch Logs](billing-alert-topic/screenshots/cloudwatch-logs-billing.png)

---

# Step 9: Testing Tip (Important)

For testing purposes, set:

THRESHOLD = 0

This ensures:

- Billing will always be greater than 0  
- SNS alert will always trigger  
- Easy verification of setup  

---

## Example Output

CloudWatch Logs:

Current Billing: $0.0 
Alert sent!

---

⚠️ After testing, change it back:

THRESHOLD = 50

Otherwise, you will receive alerts every day.

# Folder Structure

```
aws-billing-alert/
│
├── README.md
├──lambda_function.py
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