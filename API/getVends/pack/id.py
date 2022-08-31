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

    def getLastBQ(self):
        from google.cloud import bigquery
        #import os
        #os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="../../../vmgc-bigquery.json"
        client = bigquery.Client()
        query_job = client.query(
            """
            SELECT
            max(id) as lastid
            FROM `vmgc-e-commerce.verti_raw.vends`
            """
        )
        results = query_job.result()  # Waits for job to complete.

        for row in results:
            lastid=row.lastid  

        self.id = lastid 
        return lastid