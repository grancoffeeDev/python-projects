class getter:
    
    def set(self, caller, endpoint ):
        self.caller = caller
        self.endpoint = endpoint
        
    def get(self, **kwargs):
        global status
        self.parametros=kwargs.items()
        api_endpoint = self.endpoint
        parametros = self.parametros
        #print(parametros)
        r=self.caller
        result = r.getData(api_endpoint,parametros)
        status = r.status
        dados = result
        if status<300:
            result = dados
        else: 
            result = 'Erro:'+str(status)
        
        return result
