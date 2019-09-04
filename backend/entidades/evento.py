from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship

from base import Base

class Evento(Base):
    '''
    Relacao one to many com vaga
    '''
    __tablename__ = 'evento'

    id = Column(Integer, primary_key=True)
    tipo = Column(Integer)
    data = Column(Date)
    vaga_id = Column(Integer, ForeignKey('vaga.id'))

    def __init__(self, tipo, data):
        self.tipo = tipo
        self.data = data