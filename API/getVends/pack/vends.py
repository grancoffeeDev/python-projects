from pack.rest_call import rest_call as call
from pack.util import util
class vends:
    def __init__(self,caller,start_date=None,end_date=None,per_page=1000,vend_id_greater_than=None,page=None) -> None:
        self.start_date = start_date
        self.end_date = end_date
        self.per_page = per_page
        self.vend_id_greater_than = vend_id_greater_than
        self.page = page
        self.caller=caller
        #self.status = status
        
    def getVends(self):
        global status
        api_endpoint = "vends"
        parametros = {'per_page': self.per_page }
        if(self.start_date!=None):
            parametros = util.somaDict(parametros,{"start_date" : self.start_date})
        if(self.end_date!=None):
            parametros = util.somaDict(parametros,{"end_date" : self.end_date})
        if(self.vend_id_greater_than!=None):
            parametros= util.somaDict(parametros,{"vend_id_greater_than" : self.vend_id_greater_than})
        if(self.page!=None):
            parametros= util.somaDict(parametros,{"page" : self.page})
    
        v=self.caller
        vend = v.getData(api_endpoint,parametros)
        status = v.status
        dados = vend
        if status<300:
            result = dados
        else: 
            result = 'Erro:'+str(status)
        
        return result
