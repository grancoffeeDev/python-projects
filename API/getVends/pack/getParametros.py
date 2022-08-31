import json as json

class parametros:
    
    def __init__(self,arquivo=None) -> None:
        if arquivo==None:
            arquivo = "parametros.json"
        self.arquivo = arquivo

    def getAll(self):
        a = self.lerArquivo()
        print (a)    
    
    def lerArquivo(self):
        conteudo = ""
        try:
            with open(self.arquivo,'r') as arq:
                conteudo = json.load(arq) 
        except:
            print("Erro Leitura dos parametros, verifique o arquivo:"+self.arquivo)
        return conteudo
    
    def get(self,parametro):
        parametros = self.lerArquivo()
        try:
            
            retorno = parametros[parametro]
        except:
            retorno = "Parametro não encontrado:"+parametro 
        return retorno
            