from pack.vends import vends as vendas
from pack.rest_call import rest_call as call
from pack.util import util as u
from pack.id import lastid as lastid
from pack.gcs import gcs
from pack.pubsub import pubsub
import functions_framework
from jsonmerge import merge as m
import pandas as pd

def maxID(data):
    df = None
    df = pd.DataFrame(data)
    return int(df['id'].max())

def removeDuplicates(data):
    df = data
    j = df.drop_duplicates(subset=['id'])
    return j.to_dict()

def CountID(data):
    df = None
    df = pd.DataFrame(data)
    return int(df['id'].count())

@functions_framework.cloud_event
def getVends(cloud_event=None): 
    api_url = "http://vmpay.vertitecnologia.com.br/api/v1"
    api_token = "DQfDYxCRstr7Ti2KSu5VouW3JzLqtuNZpMXNNvm8"    
    id = lastid()
    j2p = u()
    #g = gcs()   
    g = gcs("vmgc-gcs.json") 
    g.set("vmgc-e-commerce","gc_rawdata", "telemetria/verti/vends/") # Define dados para salvação no Bucket
    ps = pubsub("../vmgc-pubsub.json")
    #ps = pubsub()    
    ps.set("vmgc-e-commerce","lastid")
    id_salvo = ps.get("lastid") 
    id.set(id_salvo)
    print(id_salvo)

    i=0
    json_result = []
    df_vends =[]
    df_vendsAppend=[]
    df_result=[]
    last_id = int(id.get())+1
    
    caller = call(api_url,api_token)
    while True:
        i=i+1
        v=vendas(caller,None,None,1000,last_id,i)
        json_result = v.getVends()
        if json_result==[] or caller.status>300:
            if i>1:
                i=i-1
            break

        # Concat Json usando jsonmerge
        if i>1:
            df_vendsAppend =  json_result
            df_result = m(df_vends,df_vendsAppend)  
            df_vends = df_result            
        else:
            df_vends = json_result

    if df_vends!=[]:
        remote_file = str(last_id)+"-"+str(i)
        arquivo = remote_file + ".json"
        # Converte dados JSON em JSONL e envia para o GCS
        j2l = j2p.json2jsonl(df_vends) # Conversão de dos dados em JSONL (Formato aceito pelo Google BigQuery)
        g.upload_blob(j2l,arquivo) # Cria o arquivo Json direto no Cloud Storage
        # Obtem o Ultimo ID de venda obtido nos dados  
        last_id = maxID(df_vends)    
        l2 = str(last_id) 
        # Seta LastID na Fila do Pub/Sub
        ps.send(int(l2))
    return
getVends()    