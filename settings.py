import sys
BUCKET_NAME = "aub3visualsearch"
PREFIX = "test"
USER = "ubuntu"
HOST = "54.172.71.127"
private_key =  "~/.ssh/cs5356"
CONFIG_PATH = __file__.split('settings.py')[0]
AWS = sys.platform != 'darwin'
INDEX_PATH = "/mnt/*.npy" if AWS else "/Users/aub3/index/3*.npy"
DATA_PATH ="/home/ubuntu/dataset/" if AWS else "/Users/aub3/target/"