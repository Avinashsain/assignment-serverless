# Assignment 8: Sentiment Analysis Using AWS Lambda & Amazon Comprehend

---

## Objective
Automatically analyze and categorize the sentiment of user reviews using Amazon Comprehend.

---

## Services Used
- AWS Lambda
- Amazon Comprehend
- IAM
- CloudWatch Logs

---

## Project Structure

assignment-sentiment-analysis/
│
├── README.md
├── lambda_function.py
└── screenshots/
    ├── 1-iam-role.png
    ├── 2-lambda-create.png
    ├── 3-code.png
    ├── 4-test-event.png
    └── 5-cloudwatch-logs.png

---

## Step-by-Step Implementation

### Step 1: Create IAM Role

1. Go to IAM Dashboard
2. Click Roles → Create Role
3. Select AWS Service → Lambda
4. Attach Policy: ComprehendFullAccess, CloudWatchFullAccess
5. Name: Lambda-Comprehend-Role

Screenshot:
![IAM Role](screenshots/1-iam-role.png)

---

### Step 2: Create Lambda Function

1. Go to AWS Lambda
2. Click Create Function
3. Choose:
   - Author from scratch
   - Runtime: Python 3.x
4. Assign IAM Role

Screenshot:
![Lambda Create](screenshots/2-lambda-create.png)

---

### Step 3: Add Lambda Code

```python
import json
import boto3

comprehend = boto3.client('comprehend')

def lambda_handler(event, context):
    try:
        # 1. Get review text from event
        review_text = event.get("review", "")

        if not review_text:
            return {
                "statusCode": 400,
                "body": "No review text provided"
            }

        # 2. Call Amazon Comprehend
        response = comprehend.detect_sentiment(
            Text=review_text,
            LanguageCode='en'
        )

        sentiment = response['Sentiment']
        score = response['SentimentScore']

        # 3. Log result
        print(f"Review: {review_text}")
        print(f"Sentiment: {sentiment}")
        print(f"Scores: {score}")

        # 4. Return response
        return {
            "statusCode": 200,
            "review": review_text,
            "sentiment": sentiment,
            "score": score
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            "statusCode": 500,
            "error": str(e)
        }
```

Screenshot:
![Lambda Code](screenshots/3-code.png)

---

### Step 4: Test Lambda Function

#### Sample Input

```json
{
  "review": "Excellent service and very fast delivery!"
}
```

Screenshot:
![Test Event](screenshots/4-test-event.png)

---

### Step 5: Verify Output in CloudWatch

1. Go to Monitor Tab
2. Click View Logs in CloudWatch
3. Check sentiment output

Screenshot:
![CloudWatch Logs](screenshots/5-cloudwatch-logs.png)

---

## Sample Output

```json
{
  "statusCode": 200,
  "sentiment": "POSITIVE"
}
```

---

## Conclusion
This project demonstrates how to use AWS Lambda with Amazon Comprehend to automatically analyze user review sentiment in real-time.
