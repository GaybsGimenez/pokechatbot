from app.db import SessionLocal
from app.models_db import Mensagem, Sessao
from sqlalchemy.orm import Session
from openai import OpenAI
from datetime import datetime
import os


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Salva uma nova mensagem
# def salvar_mensagem(sessao_id: str, role: str, conteudo: str):
#     db = SessionLocal()
#     msg = Mensagem(sessao_id=sessao_id, role=role, conteudo=conteudo)
#     db.add(msg)
#     db.commit()
#     db.close()

def salvar_mensagem(sessao_id: str, role: str, conteudo: str):
    db = SessionLocal()

    # Garante que a sessão exista
    sessao = db.query(Sessao).get(sessao_id)
    if not sessao:
        sessao = Sessao(id=sessao_id, criado_em=datetime.utcnow())
        db.add(sessao)
        db.commit()

    msg = Mensagem(sessao_id=sessao_id, role=role, conteudo=conteudo)
    db.add(msg)
    db.commit()
    db.close()

# Pega as últimas N mensagens de uma sessão
# def get_historico(sessao_id: str, limite: int = 10):
#     db = SessionLocal()
#     mensagens = db.query(Mensagem).filter_by(sessao_id=sessao_id).order_by(Mensagem.criado_em.desc()).limit(limite).all()
#     db.close()
#     return reversed(mensagens)  # mantém ordem cronológica

def get_historico(sessao_id: str, limite: int = 10):
    db = SessionLocal()
    mensagens = db.query(Mensagem).filter_by(sessao_id=sessao_id).order_by(Mensagem.criado_em.desc()).limit(limite).all()
    db.close()
    return list(reversed(mensagens))  # agora é uma lista real com len()



# Resumir a sessão e salvar
def resumir_sessao(sessao_id: str):
    db = SessionLocal()
    mensagens = db.query(Mensagem).filter_by(sessao_id=sessao_id).order_by(Mensagem.criado_em).all()

    conteudo = "\n".join([f"{m.role}: {m.conteudo}" for m in mensagens])
    prompt = f"Resuma o seguinte diálogo em até 5 frases úteis para manter contexto de uma conversa com um treinador Pokémon:\n\n{conteudo}"
    resposta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    ).choices[0].message.content.strip()

    # Salva resumo
    sessao = db.query(Sessao).get(sessao_id)
    if not sessao:
        sessao = Sessao(id=sessao_id, resumo=resposta)
        db.add(sessao)
    else:
        sessao.resumo = resposta
    db.commit()
    db.close()
    return resposta

def obter_resumo(sessao_id: str):
    db = SessionLocal()
    sessao = db.query(Sessao).get(sessao_id)
    db.close()
    return sessao.resumo if sessao else None


