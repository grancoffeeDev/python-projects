import requests
from pack.util import util
class rest_call:
    def __init__(self,url,token) -> None:
        self.parametros = {'access_token':token }
        self.url = url

    def url(self):
        return self.url

    def parametros(self):
        return self.parametros

    def set(self,url,token):
        self.parametros = {'access_token':token }
        self.url = url

    def getData(self, modulo, module_parametros):
        url_full = self.url+"/"+modulo
        parametros = util.somaDict(self.parametros,module_parametros)
        self.parametros = parametros
        global status
        try:
            response = requests.get(url_full,params=parametros)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)    
            exit 
        status = response.status_code
        self.status = status
        resposta = response.json()
        return resposta
