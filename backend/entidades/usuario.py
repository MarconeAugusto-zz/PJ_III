from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum
from datetime import date

from base import Base

associacao_usuario_vaga = Table(
    'usuario_vaga', Base.metadata,
    Column('idUsuario', Integer, ForeignKey('usuario.id')),
    Column('idVaga', Integer, ForeignKey('vaga.id'))
)
        

class TipoUsuario(object):
    ADM = 1
    USUARIO = 2

    tipo_str = {
        ADM: 'Administrador',
        USUARIO: 'Usuario'
    }

class Usuario(Base):
    '''
    relacao many to many com vaga
    '''
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True)
    nome = Column(String(30))
    sobrenome = Column(String(30))
    login = Column(String(50), nullable=False, unique=True)
    senha = Column(String(20))
    tipo = Column(Integer)
    data_cadastro = Column(Date)
    vagas = relationship("Vaga", secondary=associacao_usuario_vaga)

    def __init__(self, nome, sobrenome, login, senha, tipo):
        self.nome = nome
        self.sobrenome = sobrenome
        self.login = login
        self.senha = senha
        self.tipo = tipo
        self.data_cadastro = date.today()
        vagas = []