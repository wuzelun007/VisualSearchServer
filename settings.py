import boto3,botocore
from boto3.session import Session
import sys
session = Session()
s3 = session.resource('s3')
s3_client = session.client('s3')
BUCKET_NAME = "aub3visualsearch"
BUCKET = s3.Bucket(BUCKET_NAME)
AMI = ''
USER = "ubuntu"
HOST = "52.90.223.78"
private_key =  "~/.ssh/cs5356" # "~/.ssh/cornellaub3nca.pem" #
CONFIG_PATH = __file__.split('settings.py')[0]
AWS = sys.platform != 'darwin'
INDEX_PATH = "/home/ubuntu/index/*.npy" if AWS else "/Users/aub3/index/3*.npy"