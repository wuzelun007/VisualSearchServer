import os,sys,logging,time
from fabric.state import env
from fabric.api import env,local,run,sudo,put,cd,lcd,puts,task,get,hide
from settings import BUCKET_NAME
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


# run('aws s3 cp s3://aub3visualsearch/ /mnt/ --recursive') # --request-payer "requester"  is not supported by AWS-CLI

@task
def notebook():
    """
    Run IPython notebook on an AWS server
    run("openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout mycert.key -out mycert.pem")
    c = get_config()
    c.NotebookApp.open_browser = False
    c.NotebookApp.ip = '0.0.0.0'
    c.NotebookApp.port = 8888
    c.NotebookApp.certfile = u'/home/ubuntu/mycert.pem'
    c.NotebookApp.enable_mathjax = False
    c.NotebookApp.password = u'{}'
    #--certfile=mycert.pem
    :return:
    """
    from IPython.lib.security import passwd
    command = "ipython notebook --ip=0.0.0.0  --NotebookApp.password={} --no-browser".format(passwd())
    print command
    run(command)



@task
def setup():
    """
    Task for initial set up of AWS instance.
    """
    sudo("chmod 777 /mnt/")
    sudo("add-apt-repository ppa:kirillshkrogalev/ffmpeg-next")
    sudo("apt-get update")
    sudo("apt-get install -y ffmpeg")
    sudo("apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927")
    sudo('echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list')
    sudo('apt-get update')
    sudo('apt-get install -y mongodb-org')
    sudo('service mongod start')

@task
def load_mongodb():
    pass







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
def server(rlocal=False):
    """
    start server
    """
    if rlocal:
        local('python server.py')
    else:
        run('python server.py')


@task
def index():
    """
    Index images
    """
    inception.load_network()
    count = 0
    start = time.time()
    with inception.tf.Session() as sess:
        for image_data in inception.get_batch():
            logging.info("Batch with {} images loaded in {} seconds".format(len(image_data),time.time()-start))
            start = time.time()
            count += 1
            features,files = inception.extract_features(image_data,sess)
            logging.info("Batch with {} images processed in {} seconds".format(len(features),time.time()-start))
            start = time.time()
            inception.store_index(features,files,count)

@task
def clear():
    """
    delete logs
    """
    local('rm logs/*.log &')


@task
def get_videos():
    with cd("/mnt/video"):
        run('youtube-dl "https://www.youtube.com/playlist?list=PLccnpqMfP0kwx4qaj1ZZw9YJtTOptmBJJ" -o "%(epoch)s.%(ext)s" --ignore-errors')

@task
def get_frames():
    videos = """
    """
    for i,v in enumerate(videos.strip().split("\n")):
        v = v.strip()
        if v:
            for i in range(500):
                command = 'ffmpeg -accurate_seek -ss {} -i /mnt/video/{}   -frames:v 1 /mnt/frames/{}.{}.jpg'.format(15.0*i,v,v,i)
                retval = run(command)
                if retval.return_code != 0:
                    break
            run('cd /mnt/frames;aws s3 mv . s3://aub3data/nyc/frames/ --recursive --storage-class "REDUCED_REDUNDANCY"')
            run('cd /mnt/video/;aws s3 mv {} s3://aub3data/nyc/videos/ --storage-class "REDUCED_REDUNDANCY"'.format(v))

