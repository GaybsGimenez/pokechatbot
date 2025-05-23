from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.parser import parse_question
from app import pokefetcher

router = APIRouter()

class PerguntaRequest(BaseModel):
    pergunta: str

@router.post("/pergunta")
def responder_pergunta(req: PerguntaRequest):
    parsed = parse_question(req.pergunta)

    action = parsed.get("action")
    pokemon = parsed.get("pokemon")

    if action == "get_types":
        return {"resposta": pokefetcher.get_types(pokemon)}
    elif action in ["get_ability", "get_primary_ability", "get_all_abilities"]:
        return {"resposta": pokefetcher.get_all_abilities(pokemon)}
    elif action == "get_weaknesses":
        return {"resposta": pokefetcher.get_weaknesses(pokemon)}
    elif action == "get_evolutions":
        return {"resposta": pokefetcher.get_evolutions(pokemon)}
    else:
        raise HTTPException(status_code=400, detail=parsed.get("message", "Pergunta não compreendida."))
