from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orcamentos = []

class Orcamento(BaseModel):
    tipo: str
    nome: str
    idade: str
    telefone: str
    detalhes: dict

@app.get("/")
def home():
    return {"message": "Sorry Mom Backend Online"}

@app.post("/orcamentos")
def criar_orcamento(orcamento: Orcamento):
    novo = {
        "id": len(orcamentos) + 1,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        **orcamento.dict()
    }

    orcamentos.append(novo)

    return {
        "status": "sucesso",
        "message": "Orçamento recebido com sucesso",
        "orcamento": novo
    }

@app.get("/orcamentos")
def listar_orcamentos():
    return orcamentos
