import os,sys,logging,time
from fabric.state import env
from fabric.api import env,local,run,sudo,put,cd,lcd,puts,task,get,hide
from settings import BUCKET_NAME,DATA_PATH,INDEX_PATH
import inception
from settings import USER,private_key,HOST
env.user = USER
env.key_filename = private_key
env.hosts = [HOST,]
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='logs/fab.log',
                    filemode='a')



@task
def notebook():
    """
    Run an IPython notebook on an AWS server
    """
    from IPython.lib.security import passwd
    command = "ipython notebook --ip=0.0.0.0  --certfile=mycert.pem --NotebookApp.password={} --no-browser".format(passwd())
    print command
    run(command)

@task
def gen_ssl():
    run("openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout mycert.key -out mycert.pem")


@task
def setup():
    """
    Task for initial set up of AWS instance.
    Used AMI modified for Python2.7 https://gist.github.com/AlexJoz/1670baf0b32573ca7923
    Following commands show other packages/libraries installed while setting up the AMI
    """
    sudo("chmod 777 /mnt/")
    sudo("add-apt-repository ppa:kirillshkrogalev/ffmpeg-next")
    sudo("apt-get update")
    sudo("apt-get install -y ffmpeg")
    run("git clone https://github.com/AKSHAYUBHAT/VisualSearchServer")
    sudo("pip install fabric")
    sudo("pip install --upgrade awscli")
    sudo("pip install --upgrade fabric")
    sudo("pip install --upgrade flask")
    sudo("pip install --upgrade ipython")
    sudo("pip install --upgrade jupyter")
    sudo("apt-get install -y python-scipy")
    sudo("apt-get install -y libblas-dev liblapack-dev libatlas-base-dev gfortran")
    sudo("pip install --upgrade nearpy")



@task
def connect():
    """
    Creates connect.sh for the current host
    :return:
    """
    fh = open("connect.sh",'w')
    fh.write("#!/bin/bash\n"+"ssh -i "+env.key_filename+" "+"ubuntu"+"@"+HOST+"\n")
    fh.close()


@task
def server():
    """
    start server
    """
    local('python server.py')


@task
def demo_fashion():
    """
    Start Demo using precomputed index for 450 thousand images.
    """
    local('aws s3api get-object --bucket aub3visualsearch --key "fashion_index.tar.gz" --request-payer requester /mnt/fashion_index.tar.gz')
    local('cd /mnt/;tar -zxvf fashion_index.tar.gz')
    local('echo "\nDEMO=\'fashion_images\'" >> settings.py')
    local('echo "\nINDEX_PATH=\'/mnt/fashion_index/\'" >> settings.py')
    local('python server.py &')
    local('tail -f logs/server.log')




@task
def index():
    """
    Index images
    """
    logging.info("Starting with images present in {} storing index in {}".format(DATA_PATH,INDEX_PATH))
    try:
        os.mkdir(INDEX_PATH)
    except:
        print "Could not created {}, if its on /mnt/ have you set correct permissions?".format(INDEX_PATH)
        raise ValueError
    inception.load_network()
    count = 0
    start = time.time()
    with inception.tf.Session() as sess:
        for image_data in inception.get_batch(DATA_PATH):
            logging.info("Batch with {} images loaded in {} seconds".format(len(image_data),time.time()-start))
            start = time.time()
            count += 1
            features,files = inception.extract_features(image_data,sess)
            logging.info("Batch with {} images processed in {} seconds".format(len(features),time.time()-start))
            start = time.time()
            inception.store_index(features,files,count,INDEX_PATH)

@task
def clear():
    """
    delete logs
    """
    local('rm logs/*.log &')


