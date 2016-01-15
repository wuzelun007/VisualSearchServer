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


####Run server 
The easiest way to use the code is to launch "ami-537b2339" in AWS North Virginia (us-east-1) region.     
The AMI contains 450,000 images and computed index. Make sure that you keep port 9000 open.
Once logged in run following commands.

 ```
  cd server
  git pull
  sudo pip install fabric
  python server.py &
  tail -f logs/server.log
```

####Index images

- configure AWS cli, using aws configure   
- We strongly recommended using IAM roles, rather than manually entering credentials. 
- set BUCKET_NAME and PREFIX in settings.py    
- copy images in \~\/Dataset folder   


 ```
  sudo pip install fabric
  fab index &
  tail -f logs/worker.log
```


#### Following libraries & templates are used:
1. https://almsaeedstudio.com/
2. http://fabricjs.com/kitchensink/
3. https://github.com/karpathy/convnetjs
4. https://www.tensorflow.org/ 
5. http://nearpy.io/

   
License:    
Copyright 2015, Cornell University. 
