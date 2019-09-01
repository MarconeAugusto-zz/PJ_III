from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from enum import Enum

from base import Base
from autenticador import Autenticador, EstadoAutenticador

class TipoVaga(Enum):
    COMUM = 1
    PREFERENCIAL = 2

class EstadoVaga(Enum):
    LIVRE = 1
    OCUPADA = 2

class Vaga(Base):
    '''
    relacao many to many com usuario
    relacao one to one com autenticador
    '''
    __tablename__ = 'vaga'

    id = Column(Integer, primary_key=True)
    tipo = Column(Integer)
    identificador = Column(String)
    autenticador = relationship("Autenticador", uselist=False, back_populates="vaga")

    def __init__(self, tipo=1, status=1, identificador=None):
        self.tipo = tipo
        self.status = status
        self.identificador = identificador