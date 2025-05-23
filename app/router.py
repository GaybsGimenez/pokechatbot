# app/router.py
from fastapi import APIRouter, Request
from pydantic import BaseModel
from app.parser import parse_question
from app import pokefetcher
from app.memory import salvar_mensagem, get_historico, obter_resumo, resumir_sessao

router = APIRouter()

class PerguntaRequest(BaseModel):
    pergunta: str
    sessao_id: str

@router.post("/pergunta")
def responder_pergunta(req: PerguntaRequest, request: Request):
    salvar_mensagem(req.sessao_id, "user", req.pergunta)

    historico = get_historico(req.sessao_id)
    resumo = obter_resumo(req.sessao_id)

    mensagens = []
    if resumo:
        mensagens.append({"role": "system", "content": f"Resumo da conversa: {resumo}"})
    for m in historico:
        mensagens.append({"role": m.role, "content": m.conteudo})

    resposta = gerar_resposta_com_contexto(mensagens)
    salvar_mensagem(req.sessao_id, "assistant", resposta)

    # Comprimir a sessão após certo número de mensagens (ex: 10)
    if len(historico) >= 10:
        resumir_sessao(req.sessao_id)

    return {"resposta": resposta}


def gerar_resposta_com_contexto(mensagens):
    from openai import OpenAI
    import os
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=mensagens,
        temperature=0.8
    )
    return completion.choices[0].message.content.strip()
