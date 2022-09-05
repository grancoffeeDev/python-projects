
from datetime import datetime
from sqlite3 import Timestamp
from pymongo import MongoClient
#from jsonmerge import merge as m
from bson.json_util import dumps #, loads
from pack.gcs import gcs
import pandas as pd

def genfile(json_data):
    #df = pd.DataFrame(json_data)
    #j2l = df.to_json(orient='records', lines=True)
    j2l=json_data
    arquivo="vends_mongo.json"
    g = gcs("../../../vmgc-gcs.json")  
    g.set("vmgc-e-commerce","gc_rawdata", "telemetria/verti/") # Define dados para salvação no Bucket
    g.upload_blob(j2l,arquivo)    



client = MongoClient('10.100.41.8:32768',
                     username='admin',
                     password='Info@2015',
                     authSource='admin',
                     authMechanism='SCRAM-SHA-1')

#client = pymongo.MongoClient("mongodb://10.100.41.8:32768/")
 
# Database Name
db = client["Verti"]
 
# Collection Name
col = db["vends"]
 
#x = col.count_documents({"id":{"$gte":176727019,"$lte":176977737}})
#x = col.count_documents({"id":{"$gte":175859291}})
x = col.find({"id":{"$gte":176727019,"$lte":176977737}})
df_vends ={}
df_vendsAppend={}

#print (x)

df = pd.DataFrame(x)
df=df.drop(columns=['_id'])
df=df.astype({'dtget':str})

#print(df)

j2l = df.to_json(orient='records', lines=True)
genfile(j2l)
#print(j2l)

#col2list = list(x)

#json_data = dumps(col2list)

#df = pd.json_normalize(json_data,record_path=".")
#j2l = df.to_json(orient='records', lines=True)
#genfile(json_data)






#print (json_data)


#for data in x:
#    df_vendsAppend =  data
#    if df_vends=={}:
#        df_result = df_vendsAppend
#    else:
#        df_result = m(df_vends,df_vendsAppend)  
#    df_vends = df_result 
#print(df_vends)