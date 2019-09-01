from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum

from base import Base

class EstadoAutenticador(Enum):
    LIVRE_AUT_OK = 1
    LIVRE_AUT_NOK = 2
    OCUPADO_AUT_OK = 3
    OCUPADO_AUT_NOK = 4

class Autenticador(Base):
    '''
    Relacao one to one com vaga
    Relacao one to many com evento
    '''
    __tablename__ = 'autenticador'

    id = Column(Integer, primary_key=True)
    codAutenticacao = Column(String)
    estado = Column(Integer)
    vaga_id = Column(Integer, ForeignKey('vaga.id'))
    vaga = relationship("Vaga", back_populates="autenticador")
    eventos = relationship("Evento")

    def __init__(self, codAutenticacao, estado, vaga):
        self.codAutenticacao = codAutenticacao
        self.estado = estado
        self.vaga = vaga