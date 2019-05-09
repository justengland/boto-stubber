import unittest
import boto3
import botocore.session
from botocore.stub import Stubber
from s3_client import s3_client
from unittest.mock import patch, Mock, MagicMock

class s3_client_list(unittest.TestCase):
    @patch.object(boto3, "client")
    def s3_client_list_test(self, mock_client):
        stubbed_client = botocore.session.get_session().create_client('s3')
        # stubbed_client = boto3.client('s3') --- seems like this should work but does not

        stubber = Stubber(stubbed_client)
        stubber.add_response('list_objects', stub_response)
        stubber.activate()

        mock_client.return_value = stubbed_client

        client = s3_client()

        actual = client.list('cloudformation-templates-us-west-2', '')
        print('actual:', actual)

        actual_results_length = len(actual.get('Contents'))
        self.assertEqual(actual_results_length, 2)


stub_response = {
  "ResponseMetadata": {
    "RequestId": "1E389A07F82251BA",
    "HostId": "xkGfpPspp48M/aA0vJ3uR+Fy7UFm80D77w+pboIKFVf5ZU+odrgKyex1abwNDuUF2ActYdWDjLA=",
    "HTTPStatusCode": 200,
    "HTTPHeaders": {
      "x-amz-id-2": "xkGfpPspp48M/aA0vJ3uR+Fy7UFm80D77w+pboIKFVf5ZU+odrgKyex1abwNDuUF2ActYdWDjLA=",
      "x-amz-request-id": "1E389A07F82251BA",
      "date": "Wed, 08 May 2019 19:40:21 GMT",
      "x-amz-bucket-region": "us-west-2",
      "content-type": "application/xml",
      "transfer-encoding": "chunked",
      "server": "AmazonS3"
    },
    "RetryAttempts": 0
  },
  "IsTruncated": False,
  "Marker": "",
  "Contents": [
    {
      "Key": "0039952412_1416613607_Windows_Roles_And_Features.template",
      "LastModified": "2016-01-05 21:22:22+00:00",
      "ETag": "\"a9fdb9578523e82ed76e3231a6bcea8c\"",
      "Size": 9587,
      "StorageClass": "STANDARD"
    },
    {
      "Key": "0039952412_1416613611_Windows_Single_Server_Active_Directory.template",
      "LastModified": "2016-01-05 21:22:19+00:00",
      "ETag": "\"e93eb89c72252643b0ff1c0c8f1e0132\"",
      "Size": 12161,
      "StorageClass": "STANDARD"
    }],
  "Name": "cloudformation-templates-us-west-2",
  "Prefix": "",
  "MaxKeys": 1000,
  "EncodingType": "url"
}