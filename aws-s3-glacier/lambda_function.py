import boto3
from datetime import datetime, timezone, timedelta

s3 = boto3.client('s3')

BUCKET_NAME = 'assignment-archive-bucket'

def lambda_handler(event, context):
    try:
        # Calculate date 6 months ago (~180 days)
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=180)

        response = s3.list_objects_v2(Bucket=BUCKET_NAME)

        if 'Contents' not in response:
            print("No files found in bucket.")
            return

        for obj in response['Contents']:
            key = obj['Key']
            last_modified = obj['LastModified']

            # Check if file is older than 6 months
            if last_modified < cutoff_date:
                print(f"Archiving: {key}")

                # Copy object to same location with Glacier storage class
                s3.copy_object(
                    Bucket=BUCKET_NAME,
                    Key=key,
                    CopySource={'Bucket': BUCKET_NAME, 'Key': key},
                    StorageClass='GLACIER'
                )

                print(f"Archived to Glacier: {key}")

            else:
                print(f"Skipping (recent): {key}")

    except Exception as e:
        print(f"Error: {str(e)}")