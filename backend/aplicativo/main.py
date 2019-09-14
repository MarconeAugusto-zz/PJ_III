import sys
# print(sys.path)

from entidades.vaga import Vaga
from entidades.usuario import Usuario
from entidades.base import engine, Base
from apirest.aplicacao import app

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    app.run(host='0.0.0.0', debug=True)