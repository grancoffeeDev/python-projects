#from pack.vends import vends as vendas
from pack.rest_call import rest_call as call
from pack.util import util as u
from pack.id import lastid as lastid
from pack.gcs import gcs
#from pack.pubsub import pubsub
import functions_framework
from jsonmerge import merge as m
from pack.getParametros import parametros
from pack.getter import getter as getter
#from datetime import datetime, timezone
#import time

@functions_framework.cloud_event
def getVends(cloud_event=None): 
    p = parametros("parametros.json").getAll()
    id = lastid()
    i=0
    df_vends =[]
    df_vendsAppend=[]
    df_result=[]
    par ={}
    last_id = 0
    if (p["getlastid"]):
        idGeted = id.getLastBQ(q=p['query_id'])
        if idGeted == None:
            raise NameError('Não foi possivel obter o último ID!')
            exit()    
        last_id = int(idGeted)
#    last_id = 183171971
    par["vend_id_greater_than"]=last_id
#    par["end_date"]='2022-10-05 03:00:00'
#    end_date = f'{datetime.now(timezone.utc).isoformat()}'
#    par["end_date"]= end_date #f'{datetime.now():%Y-%m-%d %H:%M:%S%z}'
    par['per_page']=p['api_lines']
        
    caller = call(p['api_url'],p['api_token'])
    v = getter()
    v.set(caller,p['api_module'])
    while True:
        json_result = []
        i=i+1
        par["page"]=i
        print(i)
        print(par)
        json_result = v.get(**par)
        #time.sleep(15)
        if json_result==[] or caller.status>300:
            #if i>1:
            #    i=i-1
            break

        # Concat Json usando jsonmerge
        #if i>1:
        #    df_vendsAppend =  json_result
        #    df_result = m(df_vends,df_vendsAppend)  
        #    df_vends = df_result            
        #else:
        df_vends = json_result

        if df_vends!=[]:
            if last_id != 0: 
                remote_file = str(last_id)+"-"+str(i)
            else:
                remote_file = par["start_date"]+"-"+str(i)
                
            arquivo = remote_file + ".json"
            # Converte dados JSON em JSONL e envia para o GCS
            ut=u()
            #df_vends = ut.removeDuplicates(df_vends)
            j2l = ut.json2jsonl(df_vends,arquivo) # Conversão de dos dados em JSONL (Formato aceito pelo Google BigQuery)
#            file_json_orig = remote_file+".json"
            #j2n = ut.jsonnormalize(df_vends,file_json_orig)
            #print(j2l)
            g = gcs() 
            g.set(p['project_id'],p['bucket'], p['bucket_folder']) # Define dados para gravação no Bucket
            g.upload_blob(j2l,arquivo) # Cria o arquivo Json direto no Cloud Storage
            
            #ut.createLocalJsonFile(df_vends,file_json_orig)
    return

#getVends()    