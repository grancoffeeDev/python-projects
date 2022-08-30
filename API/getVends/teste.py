from pack.vends import vends as vendas
from pack.rest_call import rest_call as call
from pack.util import util as u
from pack.gcs import gcs

def getVends(cloud_event=None): 
    api_url = "http://vmpay.vertitecnologia.com.br/api/v1"
    api_token = "DQfDYxCRstr7Ti2KSu5VouW3JzLqtuNZpMXNNvm8"    
    #g = gcs("vmgc-gcs.json")
    #ps = pubsub("vmgc-pubsub.json")
    j2p = u()
    start = call(api_url,api_token)
    v=vendas(start,None,None,100)
    
    json_result = v.getVends()


    if json_result==[] or start.status>300:
       print("Sem Retorno")
       return
 
    j2l = j2p.json2jsonl(json_result)
    
    #g = gcs("vmgc-gcs.json") 
    g = gcs()    
    g.set("vmgc-e-commerce","gc_rawdata", "telemetria/verti/vends/")
    g.upload_blob(j2l,'vends_teste.json')

getVends()
