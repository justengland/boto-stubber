import unittest
import boto3
import botocore.session
from botocore.stub import Stubber
from s3_client import s3_client
from unittest.mock import patch, Mock, MagicMock

class s3_client_list(unittest.TestCase):
    @patch.object(boto3, "client")
    def s3_client_list_test(self, mock_client):
        # stubbed_client = boto3.client('s3') --- seems like this should work but does not
        stubbed_client = botocore.session.get_session().create_client('s3')
        stubber = Stubber(stubbed_client)
        stubber.add_response('list_objects', stub_s3_list_response)
        stubber.activate()
        mock_client.return_value = stubbed_client

        client = s3_client()

        actual = client.list('cloudformation-templates-us-west-2', '')
        print('actual:', actual)

        actual_results_length = len(actual.get('Contents'))
        self.assertEqual(actual_results_length, 2)

    #@patch.object(boto3, "client")
    # @patch.object(boto3, "client")

    @patch.object(boto3, "client")
    # def s3_client_complex_test(self, mock_s3_client, mock_sts_client):
    def s3_client_complex_test(self, mock_s3_client):
        stubbed_s3_client = botocore.session.get_session().create_client('s3')
        stubber_s3 = Stubber(stubbed_s3_client)
        stubber_s3.add_response('list_objects', stub_s3_list_response)
        stubber_s3.activate()

        stubbed_sts_client = botocore.session.get_session().create_client('sts')
        stubber_sts = Stubber(stubbed_sts_client)
        stubber_sts.add_response('get_caller_identity', stub_current_user_response)
        stubber_sts.activate()

        # Use a list of responses which may be simpler, but a little more brittle when the code changes
        # to allows multiple return values for multiple API's
        mock_s3_client.side_effect = [stubbed_s3_client, stubbed_sts_client]

        client = s3_client()

        actual = client.complex('cloudformation-templates-us-west-2', '')
        print('actual:', actual)

        actual_list_results_length = len(actual['list'].get('Contents'))
        self.assertEqual(actual_list_results_length, 2)

        actual_sts_user_id = actual['user']['UserId']
        self.assertEqual(actual_sts_user_id, expected_sts_user_id)

    @patch.object(boto3, "client")
    # def s3_client_complex_test(self, mock_s3_client, mock_sts_client):
    def s3_client_complex_v2_test(self, mock_s3_client):
        # using the side_effect allows me to use multiple clients, here its s3 and sts
        # to allows multiple return values for multiple API's
        def side_effect(arg):
            stubbed_client = botocore.session.get_session().create_client(arg)

            print('side_effect:', arg)

            stubber = Stubber(stubbed_client)
            if arg == 's3':
                print('side_effect:list_objects')
                stubber.add_response('list_objects', stub_s3_list_response)

            if arg == 'sts':
                print('side_effect:get_caller_identity')
                stubber.add_response('get_caller_identity', stub_current_user_response)

            stubber.activate()
            return stubbed_client

        # use a side effect function that which may be a little more complex but it is a little less brittle
        #  when code changes.
        mock_s3_client.side_effect = side_effect

        client = s3_client()

        actual = client.complex('cloudformation-templates-us-west-2', '')
        print('actual:', actual)

        actual_list_results_length = len(actual['list'].get('Contents'))
        self.assertEqual(actual_list_results_length, 2)

        actual_sts_user_id = actual['user']['UserId']
        self.assertEqual(actual_sts_user_id, expected_sts_user_id)


stub_s3_list_response = {
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

expected_sts_user_id = "123123:Justin.England@foo.bar"
stub_current_user_response = {
    "UserId": expected_sts_user_id,
    "Account": "123123",
    "Arn": "arn:aws:sts::123123:assumed-role/queen-bee/Justin.England@foo.bar",
    "ResponseMetadata": {
        "RequestId": "5297cc40-736d-11e9-b28e-8d87d836bff0",
        "HTTPStatusCode": 200,
        "HTTPHeaders": {
            "x-amzn-requestid": "5297cc40-736d-11e9-b28e-8d87d836bff0",
            "content-type": "text/xml",
            "content-length": "469",
            "date": "Fri, 10 May 2019 21:48:18 GMT"
        },
        "RetryAttempts": 0
    }
}
