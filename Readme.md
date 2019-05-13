# aws boto3 patching example
Use boto stubber to stub out responses from the AWS Api, via the python patch.object functionality. Using the Nose
testing framework.


Run example client to pull items from public s3 buckets and sts calls.
```bash
./read.py
```

Run unit tests
```bash
python3 -m nose
```

[Mocks Aren't Stubs](https://www.martinfowler.com/articles/mocksArentStubs.html)
[Boto Stubber](https://botocore.amazonaws.com/v1/documentation/api/latest/reference/stubber.html)
[Python patch.object](https://docs.python.org/3/library/unittest.mock.html#patch-object)
[Nose Testing Framework](http://pythontesting.net/framework/nose/nose-introduction/)

