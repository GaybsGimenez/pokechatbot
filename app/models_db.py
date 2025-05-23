from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Sessao(Base):
    __tablename__ = "sessoes"
    id = Column(String, primary_key=True)
    criado_em = Column(DateTime, default=datetime.utcnow)
    resumo = Column(Text)

class Mensagem(Base):
    __tablename__ = "mensagens"
    id = Column(Integer, primary_key=True)
    sessao_id = Column(String, ForeignKey("sessoes.id"))
    role = Column(String)  # "user" ou "assistant"
    conteudo = Column(Text)
    criado_em = Column(DateTime, default=datetime.utcnow)

    sessao = relationship("Sessao", backref="mensagens")
