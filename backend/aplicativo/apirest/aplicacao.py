import sys
print(sys.path)
from flask import Flask, Blueprint
from apirest.api_usuario import bp_usuario
from apirest.api_vaga import bp_vaga


# app = App('app', __name__)
app = Flask(__name__)
app.register_blueprint(bp_usuario)
app.register_blueprint(bp_vaga)