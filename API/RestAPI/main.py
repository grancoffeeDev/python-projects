from fastapi import FastAPI
from sqlalchemy import create_engine  
from sqlalchemy import Column, String  
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker
import json
import pandas as pd


db_string = "postgresql+psycopg2://postgres:VnBgPQbYzwa95VDm@34.95.183.152:5432/TelemetriaGC"
db = create_engine(db_string)
base = declarative_base()

class gc_teste(base):  
    __tablename__ = 'gc_teste'
    nome = Column(String, primary_key=True)

Session = sessionmaker(db)  
session = Session()

base.metadata.create_all(db)
teste = session.query(gc_teste)  

x=0
dados={}
for i in teste:
    x=x+1
    dados['id']=x
    dados['nome']=i.nome

print(dados)

df = pd.DataFrame(dados)
#dados = df.to_dict()
#print(dados)
#[r.nome for r in teste]


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/teste")
async def root():
    
    return {json.loads(dados)}