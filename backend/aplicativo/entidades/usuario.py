from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum
from datetime import date

from entidades.base import Base

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
    vagas = relationship("Vaga", secondary=associacao_usuario_vaga, backref='usuario')

    def __init__(self, nome, sobrenome, login, senha, tipo):
        self.nome = nome
        self.sobrenome = sobrenome
        self.login = login
        self.senha = senha
        self.tipo = tipo
        self.data_cadastro = date.today()
        vagas = []

    def setaVagas(self, vagas):
        if type(vagas) == list:
            self.vagas.extend(vagas)
        elif vagas is not None:
            self.vagas.append(vagas)

    def obtemVagas(self):
        return self.vagas

    def converteParaJson(self, comVagas=False):
        usuarioJson = {
            'id': self.id,
            'nome': self.nome,
            'sobrenome': self.sobrenome,
            'login': self.login,
            'senha': self.senha,
            'tipo': TipoUsuario.tipo_str[self.tipo],
            'dataCadastro': self.data_cadastro
        }

        if comVagas:
            usuarioJson['vagas'] = [vg.converteParaJson() for vg in self.vagas]

        return usuarioJson