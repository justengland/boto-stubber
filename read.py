import json
from s3_client import s3_client

client = s3_client()

# Sample s3 call
# result = client.list('cloudformation-templates-us-west-2')

# Sample s3 with prefixes
# result = client.list('1000genomes', 'data/')

result = client.complex('cloudformation-templates-us-west-2')

print(json.dumps(result, default=str,indent=2))


