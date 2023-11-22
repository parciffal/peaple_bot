import boto3
from botocore.exceptions import ClientError
from datetime import datetime


class AWSTools:
    def __init__(self):
        self.BUCKET_NAME = "linkedin-bot-bucket"
        self.LOCAL_DATA_FOLDER = "data/input/"
        self.init_s3()

    def init_s3(self):
        self.s3 = boto3.client("s3")

    def upload_output_to_s3(self, filename):
        try:
            resp = self.s3.upload_file(
                filename, self.BUCKET_NAME , "outputs/{}".format(filename.split("/")[-1])
            )
        except ClientError as e:
            print(e)

    def get_input_from_bucket(self, username):
        self.s3.download_file(self.BUCKET_NAME, "inputs/{}_input.csv".format(username), "{}/{}".format(self.LOCAL_DATA_FOLDER, "{}_input.csv".format(username)))


if __name__ == "__main__":
    aws = AWSTools()
    # aws.upload_to_s3("test.txt")
    aws.get_from_bucket("input small new 01.csv")
