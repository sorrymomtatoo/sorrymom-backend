from fastapi import FastAPI, Query
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

agenda_ocupada = {
    "douglas": {
        "2026-05-10": ["10:00", "14:00", "16:00"],
    },
    "piercing": {
        "2026-05-10": ["11:00", "15:00"],
    }
}

dias_bloqueados = {
    "2026-05-12": "Estúdio fechado para manutenção.",
}

horarios_base = [
    "09:00", "10:00", "11:00", "12:00",
    "14:00", "15:00", "16:00", "17:00",
    "18:00", "19:00"
]

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

@app.get("/agenda")
def consultar_agenda(
    profissional: str = Query(...),
    data: str = Query(...)
):
    if data in dias_bloqueados:
        return {
            "profissional": profissional,
            "data": data,
            "bloqueado": True,
            "motivo": dias_bloqueados[data],
            "horarios": []
        }

    ocupados = agenda_ocupada.get(profissional, {}).get(data, [])

    horarios = []
    for hora in horarios_base:
        horarios.append({
            "hora": hora,
            "status": "busy" if hora in ocupados else "free"
        })

    return {
        "profissional": profissional,
        "data": data,
        "bloqueado": False,
        "horarios": horarios
    }
