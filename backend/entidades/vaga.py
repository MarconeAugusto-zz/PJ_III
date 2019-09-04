from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from enum import Enum

from base import Base

class TipoVaga(object):
    COMUM = 1
    PREFERENCIAL = 2

    tipo_str = {
        COMUM: 'Comum',
        PREFERENCIAL: 'Preferencial'
    }

class EstadoVaga(object):
    LIVRE_AUT_OK = 1
    LIVRE_AUT_NOK = 2
    OCUPADO_AUT_OK = 3
    OCUPADO_AUT_NOK = 4

    estado_str = {
        LIVRE_AUT_OK: 'Livre AUT OK',
        LIVRE_AUT_NOK: 'Livre AUT NOK',
        OCUPADO_AUT_OK: 'Ocupado AUT OK',
        OCUPADO_AUT_NOK: 'Ocupado AUT NOK'
    }

class Vaga(Base):
    '''
    relacao many to many com usuario
    '''
    __tablename__ = 'vaga'

    id = Column(Integer, primary_key=True)
    identificador = Column(String(50), nullable=False, unique=True)
    codAutenticacao = Column(String)
    estado = Column(Integer)
    tipo = Column(Integer)
    eventos = relationship("Evento")

    def __init__(self, identificador, codAutenticacao, estado=1, tipo=1):
        self.identificador = identificador
        self.codAutenticacao = codAutenticacao
        self.estado = estado
        self.tipo = tipo