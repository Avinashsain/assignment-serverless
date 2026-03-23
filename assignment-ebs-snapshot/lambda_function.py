import boto3
from datetime import datetime, timezone, timedelta

ec2 = boto3.client('ec2')

VOLUME_ID = "vol-xxxxxxxx"  # replace with your volume id
RETENTION_DAYS = 30

def lambda_handler(event, context):
    
    # Step 1: Create snapshot
    description = f"Automated snapshot for {VOLUME_ID} on {datetime.now(timezone.utc)}"
    
    snapshot = ec2.create_snapshot(
        VolumeId=VOLUME_ID,
        Description=description
    )
    
    snapshot_id = snapshot['SnapshotId']
    print(f"Created Snapshot: {snapshot_id}")
    
    # Step 2: Get all snapshots of this volume
    snapshots = ec2.describe_snapshots(
        Filters=[
            {'Name': 'volume-id', 'Values': [VOLUME_ID]}
        ],
        OwnerIds=['self']
    )
    
    # Step 3: Delete old snapshots
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