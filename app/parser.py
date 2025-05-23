import os
import json
from openai import OpenAI
from app.llm_config import LLM_CONFIG

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def parse_question(question: str) -> dict:
    prompt = f"""
Você é um assistente que transforma perguntas sobre Pokémon em comandos estruturados.
Use sempre um dos seguintes valores fixos para "action": get_types, get_ability, get_evolutions ou get_weaknesses.
Mesmo que haja múltiplos tipos, habilidades ou evoluções, sempre use apenas um desses valores.


Exemplos:
Q: Quais os tipos do Charizard?
A: {{"action": "get_types", "pokemon": "charizard"}}

Q: Qual a habilidade do Pikachu?
A: {{"action": "get_ability", "pokemon": "pikachu"}}

Q: Quantas evoluções tem o Bulbasaur?
A: {{"action": "get_evolutions", "pokemon": "bulbasaur"}}

Q: O Gyarados é fraco contra que tipo?
A: {{"action": "get_weaknesses", "pokemon": "gyarados"}}

Q: {question}
A:"""

    response = client.chat.completions.create(
        model=LLM_CONFIG["model"],
        temperature=LLM_CONFIG["temperature"],
        top_p=LLM_CONFIG["top_p"],
        max_tokens=LLM_CONFIG["max_tokens"],
        messages=[{"role": "user", "content": prompt}]
    )

    resposta = response.choices[0].message.content.strip()
    print("DEBUG - Resposta do GPT:", resposta)

    try:
        return json.loads(resposta)
    except Exception as e:
        print("Erro ao interpretar resposta como JSON:", e)
        return {"action": "unknown", "message": "Pergunta não compreendida."}
