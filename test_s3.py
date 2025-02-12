import boto3
import os
from dotenv import dotenv_values

dotenv_values('.env')

# Load credentials from environment variables
ACCESS_KEY = os.getenv("ACCESS_KEY")
SECRET_KEY = os.getenv("SECRET_KEY_DO")
ENDPOINT_URL = os.getenv("ENDPOINT_URL")

print(ACCESS_KEY)

# Initialize S3 client
s3_client = boto3.client(
    "s3",
    endpoint_url=ENDPOINT_URL,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
)

# List available buckets (Spaces)
try:
    response = s3_client.list_buckets()
    print("✅ Credentials Verified. Available Spaces:")
    for bucket in response["Buckets"]:
        print(f"- {bucket['Name']}")
except Exception as e:
    print(e)
    print("❌ Invalid Credentials:", e)
