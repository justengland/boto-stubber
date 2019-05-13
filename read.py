#!/usr/bin/env python3

import json
from s3_client import s3_client

client = s3_client()

# Sample s3 call
result1 = client.list('cloudformation-templates-us-west-2')
print(json.dumps(result1, default=str,indent=2))
print('---------   ---------   ---------   ---------   ---------   ---------')

# Sample s3 with prefixes
result2 = client.list('1000genomes', 'data/')
print(json.dumps(result2, default=str,indent=2))
print('---------   ---------   ---------   ---------   ---------   ---------')

result3 = client.complex('cloudformation-templates-us-west-2')
print(json.dumps(result3, default=str,indent=2))


