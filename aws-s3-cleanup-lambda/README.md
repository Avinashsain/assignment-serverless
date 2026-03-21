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

![S3 Files](screenshots/s3-files.png)

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

![IAM Role](screenshots/iam-role-s3.png)

------------------------------------------------------------------------

# Step 3: Create Lambda Function

Configuration:

Function Name: s3-cleanup-function\
Runtime: Python 3.x\
Execution Role: LambdaS3CleanupRole

Screenshot

![Lambda Create](screenshots/lambda-create.png)

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

![Lambda Code](screenshots/lambda-code-s3.png)

------------------------------------------------------------------------

# Step 5: Test Lambda

1.  Click **Deploy**
2.  Click **Test**
3.  Create test event

Event Name: test

Screenshot

![Lambda Test](screenshots/lambda-test-s3.png)

------------------------------------------------------------------------

# Step 6: Verify Results

After running Lambda:

  File Age             Result
  -------------------- ---------
  Older than 30 days   Deleted
  Newer than 30 days   Remains

Screenshot

![S3 Result](screenshots/s3-result.png)

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