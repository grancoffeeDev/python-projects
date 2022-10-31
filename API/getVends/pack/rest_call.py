import requests
from pack.util import util
import httpx

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
        if (module_parametros!=None):
            self.parametros.update(module_parametros)
        parametros=self.parametros
        global status
        #print(parametros)
        response = None
        resposta = None
        try:
            response = requests.get(url_full,params=parametros)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)    
            exit 
        status = response.status_code
        self.status = status
        resposta = response.json()
        return resposta

    def getDataX(self, modulo, module_parametros):
        url_full = self.url+"/"+modulo
        if (module_parametros!=None):
            self.parametros.update(module_parametros)
        parametros=self.parametros
        header = {'Content-Type':'application/json'}
        global status
        #print(parametros)
        response = None
        resposta = None
        try:
            response = httpx.get(url_full,params=parametros, headers=header)
            print(response.url)
        except httpx.RequestError as exc:
            print(f"An error occurred while requesting {exc.request.url!r}.")
        except httpx.HTTPStatusError as exc:
            print(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")
            exit 
        status = response.status_code
        self.status = status
        resposta = response.json()
        return resposta

