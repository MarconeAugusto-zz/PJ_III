from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from entidades.base import Base

class Evento(Base):
    '''
    Relacao one to many com vaga
    '''
    __tablename__ = 'evento'

    id = Column(Integer, primary_key=True)
    tipo = Column(Integer)
    data = Column(DateTime)
    vaga_id = Column(Integer, ForeignKey('vaga.id'), nullable=False)

    def __init__(self, tipo, vaga_id, data=None):
        self.tipo = tipo
        self.vaga_id = vaga_id
        self.data = data if data is not None else datetime.now()