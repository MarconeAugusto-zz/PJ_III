from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from base import Base

class Evento(Base):
    '''
    Relacao one to many com vaga
    '''
    __tablename__ = 'evento'

    id = Column(Integer, primary_key=True)
    tipo = Column(Integer)
    data = Column(DateTime)
    vaga_id = Column(Integer, ForeignKey('vaga.id'))

    def __init__(self, tipo, data=None):
        self.tipo = tipo
        self.data = data if data is not None else datetime.now()