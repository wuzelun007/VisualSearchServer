Visual Search Server
===============

A simple implementation of Visual Search using TensorFlow, InceptionV3 model and AWS GPU instances.

This codebase implements a simple visual indexing and search system, using features derived from Google's inception 
model trained on the imagenet data. The easist way to use it is to launch following AMI using GPU enabled g2 instances.
It already contains features computed on ~450,000 images (female fashion), the feature computation took 22 hours on 
a spot AWS g2 (single GPU) instance. i.e. ~ 230,000 images / 1 $ . Since I did not use batching, it might be possible to 
get even better performance.

The code implements two methods, a server that handles image search, and a simple indexer that extracts pool3 features.
Nearest neighbor search can be performed in an approximate manner using nearpy (faster) or using exact methods (slower).
 
![Alpha Screenshot](appcode/static/alpha3.png "Alpha Screenshot")     

####Running code on AWS

The easiest way to use the code is to launch "ami-b80f0ad2" in AWS North Virginia (us-east-1) region.     
Make sure that you keep port 9000 open. Once logged in run following commands.
We strongly recommended using IAM roles, rather than manually entering credentials. 
However you might need to configure AWS region "us-east-1" manually.

 ``` 
  cd VisualSearchServer
  git pull
  sudo chmod 777 /mnt/
  aws configure   

```

####Index images
The code provides a single index operation to index images using Pool3 features.
Store all images in a single directory, specify path to that directory. 
Specify path to a directory for storing indexes, an S3 bucket and prefix to backup computed features.   
```
# edit settings.py
BUCKET_NAME = "aub3visualsearch"
PREFIX = "nyc"
INDEX_PATH = "/mnt/nyc_index/" 
DATA_PATH ="/mnt/nyc_images/" # /mnt/ is mounted with instance store on AWS
```

To perform indexing run following. 
```
  cd ~/VisualSearchServer/
  fab index &
  tail -f logs/worker.log
```


####Run retrieval server  
``` 
python server.py &  
tail -f logs/server.log
```

####Run demo with precomputed index  
```
cd VisualSearchServer;
fab demo_fashion 
```

#### Following libraries & templates are used:
1. https://almsaeedstudio.com/
2. http://fabricjs.com/kitchensink/
3. https://github.com/karpathy/convnetjs
4. https://www.tensorflow.org/ 
5. http://nearpy.io/

   
License:    
Copyright 2015, Cornell University. 
