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

📸 Screenshot: EC2 instance with Auto-Stop tag

![EC2 Auto Stop](aws-ec2-lambda-automation/screenshots/ec2-auto-stop.png)

------------------------------------------------------------------------

### Instance 2

Name: `instance-start`

Tag:

  Key      Value
  -------- ------------
  Action   Auto-Start

📸 Screenshot: EC2 instance with Auto-Start tag

![EC2 Auto Start](screenshots/ec2-auto-start.png)

------------------------------------------------------------------------

# Step 2: Create IAM Role for Lambda

1.  Go to IAM Dashboard
2.  Click Roles → Create Role
3.  Choose Lambda
4.  Attach policy:

AmazonEC2FullAccess

Role Name:

LambdaEC2ManagerRole

📸 Screenshot: IAM role with EC2 permissions

![IAM Role](screenshots/iam-role.png)

------------------------------------------------------------------------

# Step 3: Create Lambda Function

1.  Open AWS Lambda Console
2.  Click Create Function
3.  Choose Author From Scratch

Settings:

Function Name: ec2-auto-manager\
Runtime: Python 3.x\
Execution Role: LambdaEC2ManagerRole

📸 Screenshot: Lambda function creation page

![Lambda Create](screenshots/lambda-create.png)

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

📸 Screenshot: Lambda code editor

![Lambda Code](screenshots/lambda-code.png)

------------------------------------------------------------------------

# Step 5: Deploy and Test Lambda

1.  Click Deploy
2.  Click Test
3.  Create test event

Event Name: test

📸 Screenshot: Lambda test execution

![Lambda Test](screenshots/lambda-test.png)

------------------------------------------------------------------------

# Step 6: Verify EC2 Results

Go back to EC2 Dashboard and check instance states.

Expected results:

  Instance         Tag          Result
  ---------------- ------------ ---------
  instance-stop    Auto-Stop    Stopped
  instance-start   Auto-Start   Running

📸 Screenshot: EC2 instances state after Lambda execution

![EC2 Result](screenshots/ec2-result.png)

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
