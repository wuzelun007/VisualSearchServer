from pymongo import MongoClient

# client = MongoClient()
#
# client.drop_database("visiondb")
# db = client["visiondb"]
#
# for line in file("car.txt"):
#     line = line.strip()
#     e = line.strip().split()
#     if e[-1].startswith("frames") and "." in line:
#         entry = {}
#         entry['key'] = e[-1]
#         fname = e[-1].split("/")[-1]
#         video,findex,_ = fname.split(".")
#         entry['video'] = video
#         entry['findex'] = int(findex)
#         entry['bucket'] = "aub3cardata"
#         db['frames'].insert(entry)
#     if e[-1].startswith("raw") and "." in line:
#         entry = {}
#         entry['key'] = e[-1]
#         fname = e[-1].split("/")[-1]
#         video,_ = fname.split(".")
#         entry['video'] = video
#         entry['dashcam'] = True
#         entry['nyc'] = False
#         entry['bucket'] = "aub3cardata"
#         db['videos'].insert(entry)
# print "loaded aub3cardata"
#
# for line in file("s3_list.txt"):
#     line = line.strip()
#     e = line.strip().split()
#     if e[-1].startswith("nyc/frames") and "." in line:
#         entry = {}
#         entry['key'] = e[-1]
#         fname = e[-1].split("/")[-1]
#         video,ext,findex,_ = fname.split(".")
#         entry['video'] = video
#         entry['findex'] = int(findex)
#         entry['bucket'] = "aub3data"
#         db['frames'].insert(entry)
#     if e[-1].startswith("nyc/videos") and "." in line:
#         entry = {}
#         entry['key'] = e[-1]
#         fname = e[-1].split("/")[-1]
#         if ".f247" in fname:
#             fname = fname.replace(".f247","_f247")
#         try:
#             video,_ = fname.split(".")
#         except:
#             print fname
#         entry['video'] = video
#         entry['dashcam'] = False
#         entry['nyc'] = True
#         entry['bucket'] = "aub3data"
#         db['videos'].insert(entry)
# print "loaded aub3data"
#
# for line in file("s3_list.txt"):
#     line = line.strip()
#     e = line.strip().split()
#     if e[-1].startswith("dataset/") and "." in line and ".DS_Store" not in line:
#         entry = {}
#         entry['key'] = e[-1]
#         fname = e[-1].split("/")[-1]
#         entry['mini'] = True
#         entry['bucket'] = "aub3data"
#         db['fashion'].insert(entry)
#     if e[-1].startswith("models/") and "." in line and ".DS_Store" not in line:
#         entry = {}
#         entry['key'] = e[-1]
#         _,model_name,fname = e[-1].split("/")
#         entry['mini'] = False
#         entry['model_name'] = model_name
#         entry['bucket'] = "aub3data"
#         db['fashion'].insert(entry)
# print "loaded aub3data"





