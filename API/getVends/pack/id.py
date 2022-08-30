class lastid:
    def __init__(self,arquivo=None) -> None:
        self.arquivo=arquivo

    def set(self,id):
        self.id = id

    def get(self):
        return self.id

    def salvar(self):
        if self.arquivo==None:
            arquivo = "lastid"
        else: arquivo = self.arquivo
        with open(arquivo+'.txt', 'w') as arq:
            arq.write(self.get())
        return None

    def ler(self):
        conteudo = ""
        if self.arquivo==None:
            arquivo = "lastid"
        else: arquivo = self.arquivo
        try:
            with open(arquivo+'.txt','r') as arq:
                conteudo = arq.read()
        except:
            self.set(str(0))
            self.salvar()
            self.ler()
            conteudo = str(0)
            print("Lendo Conteudo:"+conteudo)
        return conteudo