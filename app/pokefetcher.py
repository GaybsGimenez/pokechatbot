import requests
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
BASE_URL = "https://pokeapi.co/api/v2"


def embelezar_resposta(texto_base: str, contexto: str = "") -> str:
    prompt = f"""
Transforme a seguinte frase em uma resposta natural, divertida e cativante, como se você fosse um especialista em Pokémon falando com um treinador iniciante.

Frase base: "{texto_base}"
{f"Contexto adicional: {contexto}" if contexto else ""}
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9
    )
    return response.choices[0].message.content.strip()


def get_pokemon_data(pokemon_name: str):
    res = requests.get(f"{BASE_URL}/pokemon/{pokemon_name.lower()}")
    if res.status_code != 200:
        return None
    return res.json()


def get_types(pokemon_name: str):
    data = get_pokemon_data(pokemon_name)
    if not data:
        return f"Pokémon '{pokemon_name}' não encontrado."
    types = [t['type']['name'] for t in data['types']]
    texto_base = f"Os tipos de {pokemon_name.capitalize()} são: {', '.join(types)}."
    return embelezar_resposta(texto_base)


def get_ability(pokemon_name: str):
    data = get_pokemon_data(pokemon_name)
    if not data:
        return f"Pokémon '{pokemon_name}' não encontrado."
    ability = data['abilities'][0]['ability']['name']
    texto_base = f"A habilidade principal de {pokemon_name.capitalize()} é: {ability}."
    return embelezar_resposta(texto_base)


def get_all_abilities(pokemon_name: str):
    data = get_pokemon_data(pokemon_name)
    if not data:
        return f"Pokémon '{pokemon_name}' não encontrado."

    habilidades = []
    for ability in data['abilities']:
        nome = ability['ability']['name']
        if ability['is_hidden']:
            habilidades.append(f"{nome} (oculta)")
        else:
            habilidades.append(nome)

    texto_base = f"As habilidades de {pokemon_name.capitalize()} são: {', '.join(habilidades)}."
    return embelezar_resposta(texto_base)


def get_weaknesses(pokemon_name: str):
    data = get_pokemon_data(pokemon_name)
    if not data:
        return f"Pokémon '{pokemon_name}' não encontrado."

    type_name = data['types'][0]['type']['name']
    res = requests.get(f"{BASE_URL}/type/{type_name}")
    type_data = res.json()

    weaknesses = [t['name'] for t in type_data['damage_relations']['double_damage_from']]
    texto_base = f"{pokemon_name.capitalize()} é fraco contra os tipos: {', '.join(weaknesses)}."
    return embelezar_resposta(texto_base)


def get_evolutions(pokemon_name: str):
    species_res = requests.get(f"{BASE_URL}/pokemon-species/{pokemon_name.lower()}")
    if species_res.status_code != 200:
        return f"Pokémon '{pokemon_name}' não encontrado."
    species = species_res.json()

    evo_url = species['evolution_chain']['url']
    chain_data = requests.get(evo_url).json()['chain']

    evolutions = []
    current = chain_data
    while current:
        evolutions.append(current['species']['name'])
        current = current['evolves_to'][0] if current['evolves_to'] else None

    if len(evolutions) > 1:
        texto_base = f"{pokemon_name.capitalize()} evolui para: {', '.join(evolutions[1:])}."
    else:
        texto_base = f"{pokemon_name.capitalize()} não possui evoluções."

    return embelezar_resposta(texto_base)
