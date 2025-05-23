# PokéChatBot

PokéChatBot é um projeto pessoal de estudo.

Ele consiste em uma API interativa construída com FastAPI que responde a perguntas sobre Pokémon de forma divertida e amigável, utilizando a PokéAPI e um modelo da OpenAI (GPT-3.5). Faça perguntas como "Quais os tipos do Charizard?" ou "O Gyarados é fraco contra o quê?" e receba respostas como se estivesse conversando com um mestre Pokémon!

---

## Funcionalidades

- Descobre os **tipos** de um Pokémon
- Informa as **habilidades** (principais e ocultas)
- Lista as **fraquezas** de tipos
- Retorna as **evoluções** de um Pokémon
- Todas as respostas são **embelezadas** com ajuda da LLM para parecerem naturais e divertidas

---

## Estrutura do Projeto

```bash

POKECHATBOT/
├── app/
│   ├── llm\_config.py       # Configurações da OpenAI
│   ├── main.py             # Instância do FastAPI
│   ├── parser.py           # Interpretação da pergunta via LLM
│   ├── pokefetcher.py      # Integração com a PokéAPI
│   └── router.py           # Roteamento da API
├── tests/
│   └── test\_api.py         # Testes automatizados
├── .env                    # Chave da API da OpenAI
├── .gitignore
├── requirements.txt
└── README.md

````

---

## Requisitos

- Python 3.8+
- Conta e chave de API da [OpenAI](https://platform.openai.com/)
- Internet (para acessar a PokéAPI e OpenAI)

---

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seuusuario/pokechatbot.git
cd pokechatbot
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Crie o arquivo `.env` com sua chave da OpenAI

```bash
OPENAI_API_KEY=sua-chave-aqui
```

---

## Executando o projeto

```bash
uvicorn app.main:app --reload
```

Acesse a documentação interativa da API:
[http://localhost:8000/docs](http://localhost:8000/docs)

---

## Testes

Você pode rodar os testes com:

```bash
pytest
```

---

## Exemplo de uso

Faça um `POST` para `/pergunta` com o corpo:

```json
{
  "pergunta": "Quais os tipos do Bulbasaur?"
}
```

Resposta esperada:

```json
{
  "resposta": "Bulbasaur é um Pokémon dos tipos Grass e Poison! Uma combinação interessante e muito comum entre os iniciais da região de Kanto!"
}
```

---

## Créditos

- [PokéAPI](https://pokeapi.co/) — Dados dos Pokémon
- [OpenAI GPT](https://openai.com/) — Processamento de linguagem
- [FastAPI](https://fastapi.tiangolo.com/) — Framework da API
