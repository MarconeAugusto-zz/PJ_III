import sys
print(sys.path)
from flask import Flask, Blueprint
from apirest.api_usuario import bp_usuario


# app = App('app', __name__)
app = Flask(__name__)
app.register_blueprint(bp_usuario)