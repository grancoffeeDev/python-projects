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

        
        
 #   def getLastBQ(**kwargs):
 #       for key, value in kwargs.items():
 #           print("The value of {} is {}".format(key, value))


   
        
    def getLastBQ(self,**kwargs):
        from google.cloud import bigquery
        query = None
        credencial = None
        v=0
        for key, value in kwargs.items():
            if key=='q':
                query = value
                v=1
            if key=='credencial':
                credencial = value
                v=1
        if v==0:
            print("Erro nos parametros!")
            exit
        
        if query ==None:
            print("Informe a Query!!!")
            exit
        
        if credencial!=None:
            import os
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=credencial
        client = bigquery.Client()
        query_job = client.query(query)
        #(    """
        #    SELECT
        #    max(id) as lastid
        #    FROM `vmgc-e-commerce.verti_raw.vends`
        #    """
        #)
        results = query_job.result()  # Waits for job to complete.
        for row in results:
            lastid=row.lastid  
        self.id = lastid 
        return lastid