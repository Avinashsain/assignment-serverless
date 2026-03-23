# Assignment 4: Automatic EBS Snapshot and Cleanup Using AWS Lambda

---

## Objective
Automate EBS snapshot creation and delete snapshots older than 30 days using AWS Lambda and Boto3.

---

## Project Structure
```
assignment-ebs-snapshot/
│
├── README.md
├── lambda_function.py
├── screenshots/
│   ├── 1-ebs-volume.png
│   ├── 2-iam-role.png
│   ├── 3-lambda-function.png
│   ├── 4-lambda-code.png
│   ├── 5-test-output.png
│   ├── 6-eventbridge-rule.png
│   ├── 7-eventbridge-rule.png
│   ├── 8-cloudwatch-logs.png
│   └── 9-ec2-snapshots.png
```

---

## Step 1: EBS Volume Setup
- Created an EBS volume from EC2 dashboard
- Volume ID: `vol-xxxxxxxx`

Screenshot:
![EBS Volume](screenshots/1-ebs-volume.png)

---

## Step 2: IAM Role
- Created IAM Role for Lambda
- Attached policy: `AmazonEC2FullAccess`
- Attached policy: `CloudWatchFullAccess`

Screenshot:
![IAM Role](screenshots/2-iam-role.png)

---

## ⚡ Step 3: Lambda Function Setup
- Function Name: `ebs-snapshot-cleanup-function`
- Runtime: Python 3.x

Screenshot:
![Lambda Setup](screenshots/3-lambda-function.png)

Screenshot:
![Lambda Code](screenshots/4-lambda-code.png)

---

## Step 4: Lambda Code

```python
import boto3
from datetime import datetime, timezone, timedelta

ec2 = boto3.client('ec2')

VOLUME_ID = "vol-xxxxxxxx"  # replace with your volume id
RETENTION_DAYS = 30

def lambda_handler(event, context):
    description = f"Automated snapshot for {VOLUME_ID} on {datetime.now(timezone.utc)}"
    
    snapshot = ec2.create_snapshot(
        VolumeId=VOLUME_ID,
        Description=description
    )
    
    snapshot_id = snapshot['SnapshotId']
    print(f"Created Snapshot: {snapshot_id}")
    
    snapshots = ec2.describe_snapshots(
        Filters=[{'Name': 'volume-id', 'Values': [VOLUME_ID]}],
        OwnerIds=['self']
    )
    
    deleted_snapshots = []
    now = datetime.now(timezone.utc)
    
    for snap in snapshots['Snapshots']:
        start_time = snap['StartTime']
        age = now - start_time
        
        if age > timedelta(days=RETENTION_DAYS):
            ec2.delete_snapshot(SnapshotId=snap['SnapshotId'])
            deleted_snapshots.append(snap['SnapshotId'])
    
    print(f"Deleted Snapshots: {deleted_snapshots}")
    
    return {
        "created_snapshot": snapshot_id,
        "deleted_snapshots": deleted_snapshots
    }
```

---

## Step 5: Testing (Important)

### Temporary Changes for Testing:
To verify snapshot deletion quickly, the following changes were made:

```python
RETENTION_DAYS = 0
```

OR

```python
if age > timedelta(minutes=2):
```

### EventBridge Schedule for Testing:
```
rate(5 minutes)
```

### Result:
- Snapshot created automatically
- Snapshot deleted within 2 minutes

Screenshot:
![Test Output](screenshots/5-test-output.png)

---

## Step 6: EventBridge Trigger (Final Setup)
- Created rule using schedule:
```
rate(7 days)
```

Screenshot:
![EventBridge Rule Event Schedule](screenshots/6-eventbridge-rule.png)
![EventBridge Rule Targets](screenshots/7-eventbridge-rule.png)

---

## Step 7: CloudWatch Logs
- Verified logs for execution

Screenshot:
![CloudWatch Logs](screenshots/8-cloudwatch-logs.png)

---

## Step 8: Snapshot Verification
- Checked EC2 → Snapshots
- Confirmed:
  - New snapshot created
  - Old snapshots deleted

Screenshot:
![Snapshots](screenshots/9-ec2-snapshots.png)

---

## Output Example
```
Created Snapshot: snap-abc
Deleted Snapshots: ['snap-xyz']
```

---

## Conclusion
This project successfully automates:
- EBS snapshot creation
- Cleanup of old snapshots
- Scheduled execution using EventBridge

This reduces manual effort and optimizes storage cost.

---

## Improvements
- Use tags to filter snapshots
- Add SNS notifications
- Implement least privilege IAM role

---

## Note
After testing, ensure:
- `RETENTION_DAYS = 30`
- Schedule is set to `rate(7 days)`

---