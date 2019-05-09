import json
from s3_client import s3_client

client = s3_client()

result = client.list('cloudformation-templates-us-west-2')

# Sample s3 with prefixes
# result = client.list('1000genomes', 'data/')

print(json.dumps(result, default=str,indent=2))


