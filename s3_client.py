import boto3


class s3_client:
    """A simple s3 client, patch in a stubbed s3 object for testing"""

    # You could pass through the s3 client in the constructor to pass the stubbed client
    #  but with the patch attribute, you dont have to add this extra boiler plate
    # def __init__(self, s3=boto3.client('s3')):
    #     self.s3 = s3


    def list(self, bucket, prefix=''):
        #s3 = self.s3 - not needed with the patched approch
        s3 = boto3.client('s3')

        return s3.list_objects(Bucket=bucket)
