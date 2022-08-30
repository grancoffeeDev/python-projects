import json
import pandas as pd
import datetime

class util:
    def __init__(self) -> None:
        pass

    def somaDict(dict1,dict2):
        for i in (dict2):
            dict1[i]=dict2[i]
        return dict1
    
    def createLocalJsonFile(self,json_text,filename):
        file = filename
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(json_text, f, ensure_ascii=False, indent=4) # Pretty
            #json.dump(json_text, f)
        return

    def printJson(value,type=0):
        if type==1:
            valores = json.dumps(value,sort_keys=True, indent=4)
        else:
            valores = json.dumps(value)
        return valores   
    
    def json2parquet(self,json_text,parquet_file):
        df = pd.DataFrame(json_text)
        pf = parquet_file+".parquet"
        df.to_parquet(pf)
        return pf

    def json2jsonl(self,json_text):
        df = pd.DataFrame(json_text)
        dtget = datetime.datetime.now()
        df['dt_get'] = dtget
        j2l = df.to_json(orient='records', lines=True)
        #print(j2l)
        return j2l


