from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship

from base import Base
from autenticador import Autenticador

class Evento(Base):
    '''
    Relacao one to many com Autenticador
    '''
    __tablename__ = 'evento'

    id = Column(Integer, primary_key=True)
    tipo = Column(Integer)
    data = Column(Date)
    autenticador_id = Column(Integer, ForeignKey('autenticador.id'))

    def __init__(self, tipo, data, autenticador):
        self.tipo = tipo
        self.data = data
        self.autenticador = autenticador