from pack.vends import vends as vendas
from pack.rest_call import rest_call as call
from pack.util import util as u
from pack.id import lastid as lastid
from pack.gcs import gcs
from pack.pubsub import pubsub
import functions_framework
from jsonmerge import merge as m
from pack.getParametros import parametros
from pack.getter import getter as getter

@functions_framework.cloud_event
def getVends(cloud_event=None): 
    p = parametros("parametros.json")
    api_url = p.get("api_url") 
    api_token = p.get("api_lines")
    lin = p.get("api_token")
    project_id = p.get("project_id")
    bucket = p.get("bucket")
    bucket_folder= p.get("bucket_folder")
    getid = p.get("getlastid")
    queryid = p.get("query_id")    
    module = p.get("api_module")
    id = lastid()
    i=0
    json_result = []
    df_vends =[]
    df_vendsAppend=[]
    df_result=[]
    par ={}
    if (getid):
        idGeted = id.getLastBQ(q=queryid)
        if idGeted == None:
            raise NameError('Não foi possivel obter o último ID!')
            exit()    
        last_id = int(idGeted)
        par = {"vend_id_greater_than":last_id}
        
    caller = call(api_url,api_token)
    v = getter()
    v.set(caller,module)
    while True:
        i=i+1
        par = par.update({"lines":lin, "page":i})
#        par = {"vend_id_greater_than":last_id,"lines":lin, "page":i }
        json_result = v.get(par)
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
        ut=u()
        j2l = ut.json2jsonl(df_vends) # Conversão de dos dados em JSONL (Formato aceito pelo Google BigQuery)
        print(j2l)
        #g = gcs() 
        #g.set(project_id,bucket, bucket_folder) # Define dados para salvação no Bucket
        
        #g.upload_blob(j2l,arquivo) # Cria o arquivo Json direto no Cloud Storage
        
        # Obtem o Ultimo ID de venda obtido nos dados  
        #last_id = u.maxID(df_vends)    
        #l2 = str(last_id) 
        # Seta LastID na Fila do Pub/Sub
        #ps.send(int(l2))
    return
getVends()    