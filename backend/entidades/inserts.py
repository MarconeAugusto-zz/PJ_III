# coding=utf-8

# 1 - imports
from datetime import date

from usuario import Usuario, TipoUsuario
from base import Session, engine, Base
from vaga import Vaga, TipoVaga, EstadoVaga
from autenticador import Autenticador, EstadoAutenticador
from evento import Evento

# 2 - generate database schema
Base.metadata.create_all(engine)

# 3 - create a new session
session = Session()

# 4 - cria usuarios
usuario01 = Usuario('Joao', 'Pereira', 'joao', '1234', 1)
usuario02 = Usuario('Pedro', 'Souza', 'pedro', '4567', 2)
usuario03 = Usuario('Maria', 'Rosa', 'maria', '7890', 1)

# 5 - cria vagas
vaga01 = Vaga(1, 1, 'A01')
vaga02 = Vaga(2, 1, 'B04')
vaga03 = Vaga(1, 2, 'A18')

# 6 - adiciona vaga ao usuario
usuario01.vagas = [vaga01]
usuario02.vagas = [vaga02]
usuario03.vagas = [vaga03]

# 7 - adiciona contato aos usuarios
# contato01 = Contato('123456789', 'usuario01@email.com', '999111222', usuario01)
# contato02 = Contato('524252123', 'usuario02@email.com', '753527334', usuario02)
# contato03 = Contato('193316123', 'usuario03@email.com', '932198731', usuario03)

# 8 - cria tags
    # LIVRE_AUT_OK = 1
    # LIVRE_AUT_NOK = 2
    # OCUPADO_AUT_OK = 3
    # OCUPADO_AUT_NOK = 4
autenticador01 = Autenticador('A031DF', 1, vaga01)
autenticador02 = Autenticador('B7A912', 2, vaga02)
autenticador03 = Autenticador('82AD61', 3, vaga03)

# 9 - salva os dados
session.add(usuario01)
session.add(usuario02)
session.add(usuario03)

session.add(autenticador01)
session.add(autenticador02)
session.add(autenticador03)

# session.add(contato01)
# session.add(contato02)
# session.add(contato03)

# 10 - commit and close session
session.commit()
session.close()