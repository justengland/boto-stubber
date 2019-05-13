import boto3
import json

user = boto3.client('sts').get_caller_identity()
print(json.dumps(user, indent=4))
